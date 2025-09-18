from __future__ import annotations

from typing import Callable, Iterable

from step import Step
from postprocessing.sanitizer import Sanitizer
from postprocessing.analyze import Analyze
from postprocessing.artistfixer import ArtistFixer
from processing.converter import Converter
from processing.epsflattener import EpsFlattener
from processing.extractor import Extractor
from processing.mover import Mover
from processing.renamer import Renamer
from downloader.youtube import YoutubeDownloader
from downloader.soundcloud import SoundcloudDownloader
from downloader.telegram import TelegramDownloader
from .run_tagger import run_tagger


class LazyLoader:
    def __init__(self, factory: Callable[[], object]):
        self._factory = factory
        self._instance: object | None = None

    def get(self) -> object:
        if self._instance is None:
            instance = self._factory()
            setup = getattr(instance, "setup", None)
            if callable(setup):
                setup()
            self._instance = instance
        return self._instance


class LazyStepFactory:
    def __init__(self, name: str, condition_keys: Iterable[str], action: Callable):
        self.name = name
        self.condition_keys = tuple(condition_keys)
        self._action = action
        self._step: Step | None = None

    def __call__(self) -> Step:
        if self._step is None:
            self._step = Step(self.name, self.condition_keys, self._action)
        return self._step


# Shared lazy loaders for processors/downloaders
extractor_loader = LazyLoader(Extractor)
renamer_loader = LazyLoader(Renamer)
mover_loader = LazyLoader(Mover)
converter_loader = LazyLoader(Converter)
sanitizer_loader = LazyLoader(Sanitizer)
flattener_loader = LazyLoader(EpsFlattener)
youtube_loader = LazyLoader(YoutubeDownloader)
soundcloud_loader = LazyLoader(SoundcloudDownloader)
telegram_loader = LazyLoader(TelegramDownloader)
analyze_loader = LazyLoader(Analyze)
artist_fixer_loader = LazyLoader(ArtistFixer)


# Action callables ---------------------------------------------------------
def extractor_action() -> None:
    extractor_loader.get().run()


def renamer_action() -> None:
    renamer_loader.get().run()


def mover_action(dry_run: bool = False) -> None:
    mover_loader.get().run(dry_run=dry_run)


def converter_action() -> None:
    converter_loader.get().run()


def sanitizer_action() -> None:
    sanitizer_loader.get().run()


def flattener_action() -> None:
    flattener_loader.get().run()


def youtube_action() -> None:
    youtube_loader.get().run()


def manual_youtube_action(url: str, breakOnExisting: bool = True) -> None:
    youtube_loader.get().download_link(url, breakOnExisting=breakOnExisting)


def soundcloud_action(account: str = "", download: bool = True) -> None:
    soundcloud_loader.get().run(account=account, download=download)


def telegram_action(channel: str = "", limit: int | None = None) -> None:
    telegram_loader.get().run(channel=channel, limit=limit)


def analyze_action() -> None:
    analyze_loader.get().run()


def artist_fixer_action() -> None:
    artist_fixer_loader.get().run()


# Step factories ----------------------------------------------------------
_step_factories = [
    LazyStepFactory("Extractor", ["import", "extract"], extractor_action),
    LazyStepFactory("Renamer", ["import", "rename"], renamer_action),
    LazyStepFactory("Mover", ["import", "move"], mover_action),
    LazyStepFactory("Converter", ["convert"], converter_action),
    LazyStepFactory("Sanitizer", ["sanitize"], sanitizer_action),
    LazyStepFactory("Flattener", ["flatten"], flattener_action),
    LazyStepFactory("YouTube Downloader", ["download", "download-youtube"], youtube_action),
    LazyStepFactory("Manual YouTube Downloader", ["manual-youtube"], manual_youtube_action),
    LazyStepFactory("SoundCloud Downloader", ["download", "download-soundcloud"], soundcloud_action),
    LazyStepFactory("Telegram Downloader", ["download-telegram"], telegram_action),
    LazyStepFactory("Analyze", ["analyze"], analyze_action),
    LazyStepFactory("ArtistFixer", ["artistfixer"], artist_fixer_action),
    LazyStepFactory(
        "Tagger",
        ["tag", "tag-labels", "tag-soundcloud", "tag-youtube", "tag-generic", "tag-telegram"],
        run_tagger,
    ),
]

step_map = {key: factory for factory in _step_factories for key in factory.condition_keys}
steps_to_run = [factory() for factory in _step_factories]

__all__ = ["steps_to_run", "step_map"]
