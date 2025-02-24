import glob
import logging
import os
import sys

from mutagen import MutagenError
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4Tags

from data.settings import Settings
from postprocessing.Song.BaseSong import ExtensionNotSupportedException
from postprocessing.Song.GenericSong import GenericSong
from postprocessing.Song.LabelSong import LabelSong
from postprocessing.Song.SoundcloudSong import SoundcloudSong
from postprocessing.Song.YoutubeSong import YoutubeSong
from postprocessing.constants import SongTypeEnum

# global vars
EasyID3.RegisterTextKey('publisher_old', 'TPUB')
EasyID3.RegisterTXXXKey('publisher', 'publisher')
EasyID3.RegisterTXXXKey('parsed', 'parsed')
EasyMP4Tags.RegisterTextKey("publisher", "publisher")
EasyMP4Tags.RegisterTextKey("parsed", "parsed")

s = Settings()

parse_labels = True
parse_youtube = True
parse_soundcloud = True
parse_generic = True

parse_mp3 = True
parse_flac = True
parse_m4a = True
parse_wav = False # Wav is currently bugged, should fix
parse_aac = False # AAC does somehow not have any tags -> Changed downloads to m4a..


class Tagger:
    def __init__(self):
        pass

    def tag(self):
        logging.info("Starting Tag Step")
        if parse_labels:
            label_folders = [f for f in os.listdir(s.eps_folder_path) if
                             not os.path.isfile(os.path.join(s.eps_folder_path, f))]
            label_folders.sort()
            for label in label_folders:
                # Skip free/none and todofolder
                if label[0] != "_":
                    self.parse_folder(s.eps_folder_path + s.delimiter + label, SongTypeEnum.LABEL)
                    pass
                else:
                    self.parse_folder(s.eps_folder_path + s.delimiter + label, SongTypeEnum.GENERIC)


        if parse_soundcloud:
            soundcloud_folder = s.music_folder_path + s.delimiter + "Soundcloud"
            soundcloud_channel_folders = [f for f in os.listdir(soundcloud_folder) if
                                          not os.path.isfile(os.path.join(soundcloud_folder, f))]
            soundcloud_channel_folders.sort()
            for soundcloud_channel_folder in soundcloud_channel_folders:
                self.parse_folder(
                    s.music_folder_path + s.delimiter + "Soundcloud" + s.delimiter + soundcloud_channel_folder,
                    SongTypeEnum.SOUNDCLOUD)

        if parse_youtube:
            youtube_folder = s.music_folder_path + s.delimiter + "Youtube"
            youtube_channel_folders = [f for f in os.listdir(youtube_folder) if
                                       not os.path.isfile(os.path.join(youtube_folder, f))]
            youtube_channel_folders.sort()
            for youtube_channel_folder in youtube_channel_folders:
                self.parse_folder(
                    s.music_folder_path + s.delimiter + "Youtube" + s.delimiter + youtube_channel_folder,
                    SongTypeEnum.YOUTUBE)

        if parse_generic:
            folders = ["Livesets", "Podcasts", "Top 100", "Warm Up Mixes"]
            for folder in folders:
                generic_music_folders = [f for f in os.listdir(s.music_folder_path + s.delimiter + folder) if
                                         not os.path.isfile(
                                             os.path.join(s.music_folder_path + s.delimiter + folder, f))]
                for generic_music_folder in generic_music_folders:
                    self.parse_folder(
                        s.music_folder_path + s.delimiter + folder + s.delimiter + generic_music_folder,
                        SongTypeEnum.GENERIC)

    def parse_folder(self, folder, song_type):
        if '@eaDir' in folder:
            return

        # logging.info(folder)
        folders = [f for f in os.listdir(folder) if
                   not os.path.isfile(os.path.join(folder, f))]
        files = []
        if parse_mp3:
            files += (glob.glob(
                folder + s.delimiter + "*.mp3"))
        if parse_flac:
            files += (glob.glob(
                folder + s.delimiter + "*.flac"))
        if parse_wav:
            files += (glob.glob(
                folder + s.delimiter + "*.wav"))
        if parse_m4a:
            files += (glob.glob(
                folder + s.delimiter + "*.m4a"))
        if parse_aac:
            files += (glob.glob(
                folder + s.delimiter + "*.aac"))
        for file in files:
            try:
                self.parse_song(file, song_type)
            except KeyboardInterrupt:
                logging.info('KeyboardInterrupt')
                sys.exit(1)
            except PermissionError as e:
                logging.info(f"PermissionError: {e}, {file} ")
                pass
            except MutagenError as e:
                logging.info(f"MutagenError: {e}, {file} ")
                pass
            except FileNotFoundError as e:
                logging.info(f"FileNotFoundError: {e}, {file} ")
                pass
            except ExtensionNotSupportedException as e:
                logging.info(f"ExtensionNotSupportedException: {e}, {file} ")
                pass
            except TabError:
                pass
            except SystemExit:
                sys.exit(2)
            except Exception as e:
                logging.error(f"Parse_song failed: {e} {file}")
        for sub_folder in folders:
            if sub_folder[0] != '_':
                self.parse_folder(folder + s.delimiter + sub_folder, song_type)

    @staticmethod
    def parse_song(path, song_type):
        # logging.info(path)
        if song_type == SongTypeEnum.LABEL:
            LabelSong(path)
        if song_type == SongTypeEnum.YOUTUBE:
            YoutubeSong(path)
        if song_type == SongTypeEnum.SOUNDCLOUD:
            SoundcloudSong(path)
        if song_type == SongTypeEnum.GENERIC:
            GenericSong(path)
