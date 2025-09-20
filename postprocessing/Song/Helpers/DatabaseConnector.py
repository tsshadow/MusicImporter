import os
import time
import logging

import pymysql
from pymysql import err as pymysql_errors

class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        port = os.getenv("DB_PORT")
        try:
            self.port = int(port) if port else None
        except (TypeError, ValueError):
            logging.warning("Invalid DB_PORT value %r", port)
            self.port = None
        self.password = os.getenv("DB_PASS")
        self.db = os.getenv("DB_DB")
        # Fail fast if the database cannot be reached
        self.connect_timeout = int(os.getenv('DB_CONNECT_TIMEOUT', '5'))
        self.max_retries = int(os.getenv('DB_CONNECT_RETRIES', '5'))
        self.retry_delay = float(os.getenv('DB_CONNECT_RETRY_DELAY', '1'))

    def connect(self):
        if not all([self.host, self.user, self.password, self.db, self.port]):
            raise RuntimeError("Database connection parameters are not fully configured")
        attempt = 0
        last_error: Exception | None = None
        while attempt < max(1, self.max_retries):
            try:
                connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    connect_timeout=self.connect_timeout,
                )
                try:  # Defensive ping to ensure the socket is ready for use
                    connection.ping(reconnect=True)
                except Exception:
                    # If ping fails we fall back to retrying the full connection
                    connection.close()
                    raise
                return connection
            except (pymysql_errors.OperationalError, pymysql_errors.InterfaceError) as exc:
                last_error = exc
                attempt += 1
                logging.warning(
                    "Database connection attempt %s/%s failed: %s",
                    attempt,
                    max(1, self.max_retries),
                    exc,
                )
                if attempt >= max(1, self.max_retries):
                    break
                time.sleep(self.retry_delay * attempt)
            except Exception as exc:  # pragma: no cover - unexpected failure
                last_error = exc
                break

        if last_error:
            raise last_error
        raise RuntimeError("Unable to establish database connection")
