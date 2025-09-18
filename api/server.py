import logging
import os
import uuid
import asyncio
from contextvars import ContextVar
from datetime import datetime
from typing import Any, Dict, Optional, Set

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Header,
    WebSocket,
    WebSocketDisconnect,
    Body,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .steps import step_map
from .db_init import ensure_tables_exist

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    force=True,
)


current_job_id: ContextVar[Optional[str]] = ContextVar("current_job_id", default=None)
_default_logger = logging.LoggerAdapter(logging.getLogger(), {})
current_logger: ContextVar[logging.LoggerAdapter] = ContextVar(
    "current_logger", default=_default_logger
)


@app.on_event("startup")
def _startup() -> None:  # pragma: no cover - trivial
    print("starting up...")
    ensure_tables_exist()


class JobLogFilter(logging.Filter):
    def __init__(self, job_id: str):
        super().__init__()
        self.job_id = job_id

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - trivial
        active = current_job_id.get()
        return getattr(record, "job_id", None) == self.job_id and active == self.job_id




def _log(level, msg, *args, **kwargs):  # pragma: no cover - simple delegation
    logger = current_logger.get()
    logger.log(level, msg, *args, **kwargs)


def _exception(msg, *args, exc_info=True, **kwargs):  # pragma: no cover - simple
    _log(logging.ERROR, msg, *args, exc_info=exc_info, **kwargs)


logging.log = _log
logging.debug = lambda msg, *a, **k: _log(logging.DEBUG, msg, *a, **k)
logging.info = lambda msg, *a, **k: _log(logging.INFO, msg, *a, **k)
logging.warning = lambda msg, *a, **k: _log(logging.WARNING, msg, *a, **k)
logging.error = lambda msg, *a, **k: _log(logging.ERROR, msg, *a, **k)
logging.exception = _exception

# -----------------------------------------------------
# Security helpers
# -----------------------------------------------------
API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """Simple optional API key check."""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# -----------------------------------------------------
# CORS configuration
# -----------------------------------------------------
default_origins = (
    "http://192.168.1.178:5173,https://music-importer.teunschriks.nl"
)
trusted_origins = os.getenv("CORS_ORIGINS", default_origins).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in trusted_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


jobs: Dict[str, Dict] = {}
clients: Set[WebSocket] = set()


async def broadcast(job: Dict) -> None:
    """Send a minimal job update to all connected WebSocket clients."""
    message = {"id": job["id"], "step": job["step"], "status": job["status"]}
    disconnected: Set[WebSocket] = set()
    for connection in clients:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.add(connection)
    for connection in disconnected:
        clients.discard(connection)


def _public_job(job: Dict) -> Dict:
    return {k: v for k, v in job.items() if k not in {"task", "stop_event"}}


@app.get("/health")
async def health() -> Dict[str, str]:
    """Basic health check endpoint.

    Optionally verifies database connectivity for additional assurance.
    """
    try:
        from postprocessing.Song.Helpers.DatabaseConnector import DatabaseConnector

        def _check_db() -> None:
            conn = DatabaseConnector().connect()
            conn.close()

        await run_in_threadpool(_check_db)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail="Database connection failed") from exc
    return {"status": "ok"}


@app.get("/api/steps")
async def list_steps(_: None = Depends(verify_api_key)):
    """Return available step keys for dropdowns."""
    return {"steps": sorted(step_map.keys())}


@app.get("/api/jobs")
async def list_jobs(_: None = Depends(verify_api_key)):
    """Return jobs including completed ones."""
    return {"jobs": [_public_job(job) for job in jobs.values()]}


class JobLogHandler(logging.Handler):
    def __init__(self, job_id: str):
        super().__init__()
        self.job_id = job_id

    def emit(self, record: logging.LogRecord) -> None:
        jobs[self.job_id]["log"].append(self.format(record))


async def execute_step(
    step_name: str,
    job_id: str,
    repeat: bool,
    interval: float,
    stop_event: asyncio.Event,
    args: Dict[str, Any],
):
    job = jobs[job_id]
    step_factory = step_map.get(step_name)
    if not step_factory:
        job["status"] = "error"
        job["log"] = job.get("log", []) + [f"Unknown step: {step_name}"]
        await broadcast(job)
        return

    try:
        step = step_factory()
    except Exception as exc:
        job["status"] = "error"
        job["log"].append(f"Failed to initialize step '{step_name}': {exc}")
        await broadcast(job)
        return

    handler = JobLogHandler(job_id)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    handler.addFilter(JobLogFilter(job_id))
    job_logger = logging.getLogger(f"job.{job_id}")
    job_logger.setLevel(logging.INFO)
    job_logger.propagate = False
    job_logger.addHandler(handler)
    token_id = current_job_id.set(job_id)
    adapter = logging.LoggerAdapter(job_logger, {"job_id": job_id})
    token_logger = current_logger.set(adapter)

    try:
        job["status"] = "running"
        await broadcast(job)
        while True:
            await run_in_threadpool(step.run, {step_name}, **args)
            if stop_event.is_set() or not repeat:
                job["status"] = "done" if not stop_event.is_set() else "stopped"
                break
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                continue
        if stop_event.is_set():
            job["status"] = "stopped"
    except asyncio.CancelledError:
        job["status"] = "stopped"
        raise
    except Exception as e:  # pragma: no cover - for robustness
        job["status"] = "error"
        job["log"].append(str(e))
    finally:
        job["ended"] = datetime.utcnow().isoformat()
        await broadcast(job)
        job_logger.removeHandler(handler)
        current_logger.reset(token_logger)
        current_job_id.reset(token_id)
        job.pop("task", None)
        job.pop("stop_event", None)


@app.post("/api/run/{step_name}")
async def run_step_endpoint(
    step_name: str,
    options: Dict[str, Any] = Body(default={}),
    _: None = Depends(verify_api_key),
): 
    if step_name not in step_map:
        raise HTTPException(status_code=404, detail="Unknown step")

    if step_name == "manual-youtube" and not options.get("url"):
        raise HTTPException(status_code=400, detail="Missing url")

    repeat = bool(options.pop("repeat", False))
    interval = float(options.pop("interval", 0))
    args = options

    job_id = str(uuid.uuid4())
    stop_event = asyncio.Event()
    jobs[job_id] = {
        "id": job_id,
        "step": step_name,
        "status": "queued",
        "log": [],
        "stop_event": stop_event,
        "started": datetime.utcnow().isoformat(),
    }
    await broadcast(jobs[job_id])
    task = asyncio.create_task(
        execute_step(step_name, job_id, repeat, interval, stop_event, args)
    )
    jobs[job_id]["task"] = task
    return _public_job(jobs[job_id])


@app.get("/api/job/{job_id}")
async def get_job(job_id: str, _: None = Depends(verify_api_key)):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _public_job(job)


@app.post("/api/job/{job_id}/stop")
async def stop_job(job_id: str, _: None = Depends(verify_api_key)):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    stop_event: Optional[asyncio.Event] = job.get("stop_event")
    task: Optional[asyncio.Task] = job.get("task")
    if stop_event:
        stop_event.set()
    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    job["status"] = "stopped"
    await broadcast(job)
    return _public_job(job)


@app.websocket("/ws/jobs")
async def jobs_ws(ws: WebSocket):
    token = ws.query_params.get("api_key")
    if API_KEY and token != API_KEY:
        await ws.close(code=1008)
        return
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        clients.discard(ws)

# Serve the pre-built frontend as static files if available
frontend_dir = Path("frontend/dist")
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    logging.warning("Frontend build directory not found; static files will not be served.")
