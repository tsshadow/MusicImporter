from mutagen.id3 import ID3
from os import listdir
from os.path import isfile, join


def ignore(test):
    pass


class Scanner:

    def __init__(self, db):
        self.settings = config.Settings()
        self.db = db

    def scan(self):
        label_folders = [f for f in listdir(self.settings.eps_folder_path) if
                         not isfile(join(self.settings.eps_folder_path, f))]
        for label_folder in label_folders:
            if not '__' in label_folder:
                if not '@' in label_folder:
                    self.db.start()
                    print('start processing ' + label_folder)
                    self.process_label_folder(label_folder)
                    self.db.done()

    def process_label_folder(self, label_folder):
        # Insert the label-entry
        self.db.insert_label(label_folder)

        eps_folders = [fi for fi in listdir(self.settings.eps_folder_path + '/' + label_folder) if
                       not isfile(join(self.settings.eps_folder_path + '/' + label_folder, fi))]

        for ep_folder in eps_folders:
            self.process_ep_folder(label_folder, ep_folder)

    def process_ep_folder(self, label_folder, ep_folder):
        splitted_ep_folder = ep_folder.split(' ', 1)

        # Max length is 20, because sometime catid is not filled.
        if (len(splitted_ep_folder[0]) < 20) and (len(splitted_ep_folder) > 1):
            self.db.insert_eps(label_folder, splitted_ep_folder[0], ep_folder)
        else:
            self.db.insert_eps(label_folder, 'none', ep_folder)

        music_files = [fi for fi in listdir(self.settings.eps_folder_path + '/' + label_folder + '/' + ep_folder) if
                       isfile(join(self.settings.eps_folder_path + '/' + label_folder + '/' + ep_folder, fi))]

        for file in music_files:
            self.process_file(self.settings.eps_folder_path + "/" + label_folder + "/" + ep_folder + "/" + file,
                              label_folder, ep_folder)

    def process_file(self, filename, label, ep):
        if filename.endswith('.mp3'):
            mp3 = ID3(filename)
            # print(mp3)
            moods = self.process_file_tag(mp3, 'TMOO', self.db.insert_mood)
            artists = self.process_file_tag(mp3, 'TPE1', self.db.insert_artist, '/')
            genres = self.process_file_tag(mp3, 'TCON', self.db.insert_genre)
            album = self.process_file_tag(mp3, 'TALB', ignore)
            rating = self.process_file_tag(mp3, 'POPM:no@email', ignore)
            date = self.process_file_tag(mp3, 'TDRC', ignore)
            title = self.process_file_tag(mp3, 'TIT2', ignore)
            if len(rating) > 0 and rating[0].find('rating='):
                rating = (rating[0].split('rating=')[1].split(', ')[0])
            else:
                rating = -1

            if len(date) > 0:
                date = date[0]
            else:
                date = ''

            if len(title) > 0:
                title = title[0]
            else:
                title = ''

            if len(album) > 0:
                album = album[0]
            else:
                album = ''

            self.db.insert_song(filename, label, ep, title, album, rating, date)

            # song_mood links due to multiple moods per song
            self.process_file_tag_links(moods, filename, self.db.insert_song_mood)
            self.process_file_tag_links(artists, filename, self.db.insert_song_artist)
            self.process_file_tag_links(genres, filename, self.db.insert_song_genre)

    def process_file_tag(self, mp3, tag, database_function, split='; '):
        tags = []
        try:
            tags = str(mp3[tag]).split(split)
            for tag in tags:
                database_function(tag)
        except Exception as e:
            if tag in str(e):
                pass
            else:
                print(e)
        return tags

    def process_file_tag_links(self, tags, filename, database_function):
        if len(tags) > 0:
            for tag in tags:
                database_function(filename, tag)
