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

# instantiate processors (downloaders created on demand)
extractor = Extractor()
renamer = Renamer()
mover = Mover()
converter = Converter()
sanitizer = Sanitizer()
flattener = EpsFlattener()
analyze_step = Analyze()
artist_fixer = ArtistFixer()


def run_youtube_downloader(**kwargs):
    break_on_existing = kwargs.get("break_on_existing", True)
    YoutubeDownloader().run(break_on_existing=break_on_existing)


def run_soundcloud_downloader(**kwargs):
    break_on_existing = kwargs.get("break_on_existing", True)
    SoundcloudDownloader(break_on_existing=break_on_existing).run(account="")


def run_telegram_downloader(**kwargs):  # pragma: no cover - no options yet
    TelegramDownloader().run("")

steps_to_run = [
    Step("Extractor", ["import", "extract"], extractor.run),
    Step("Renamer", ["import", "rename"], renamer.run),
    Step("Mover", ["import", "move"], mover.run),
    Step("Converter", ["convert"], converter.run),
    Step("Sanitizer", ["sanitize"], sanitizer.run),
    Step("Flattener", ["flatten"], flattener.run),
    Step("YouTube Downloader", ["download", "download-youtube"], run_youtube_downloader),
    Step("SoundCloud Downloader", ["download", "download-soundcloud"], run_soundcloud_downloader),
    Step("Telegram Downloader", ["download-telegram"], run_telegram_downloader),
    Step("Analyze", ["analyze"], analyze_step.run),
    Step("ArtistFixer", ["artistfixer"], artist_fixer.run),
    Step(
        "Tagger",
        ["tag", "tag-labels", "tag-soundcloud", "tag-youtube", "tag-generic", "tag-telegram"],
        run_tagger,
    ),
]

step_map = {key: step for step in steps_to_run for key in step.condition_keys}

__all__ = ["steps_to_run", "step_map"]
