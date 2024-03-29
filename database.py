# Module Imports
import os
import sys

import mariadb
from dotenv import load_dotenv
from time import sleep


def connect():
    return mariadb.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        database=os.getenv('DB_DATABASE')
    )


class Database:

    def __init__(self):
        load_dotenv()
        # Connect to MariaDB Platform
        try:
            self.conn = connect()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sleep(10)
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # self.cur.execute('DROP TABLE IF EXISTS song_moods;')
        # self.cur.execute('DROP TABLE IF EXISTS song_artists;')
        # self.cur.execute('DROP TABLE IF EXISTS song_genres;')
        # self.cur.execute('DROP TABLE IF EXISTS songs;')
        # self.cur.execute('DROP TABLE IF EXISTS moods;')
        # self.cur.execute('DROP TABLE IF EXISTS artists;')
        # self.cur.execute('DROP TABLE IF EXISTS genres;')
        # self.cur.execute('DROP TABLE IF EXISTS eps;')
        # self.cur.execute('DROP TABLE IF EXISTS labels;')

        self.cur.execute('CREATE TABLE IF NOT EXISTS labels ('
                         ' id integer auto_increment not null unique,'
                         ' name varchar(255) not null unique);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS moods ('
                         ' id integer auto_increment not null unique,'
                         ' name varchar(255) unique);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS artists ('
                         ' id integer auto_increment not null unique,'
                         ' name varchar(255) unique);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS genres ('
                         ' id integer auto_increment not null unique,'
                         ' name varchar(255) unique);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS eps ('
                         ' id integer auto_increment not null unique,'
                         ' label_id integer REFERENCES labels(id),'
                         ' catid varchar(255),'
                         ' path varchar(511));')

        self.cur.execute('CREATE TABLE IF NOT EXISTS songs ('
                         ' id integer auto_increment not null unique,'
                         ' label_id integer REFERENCES labels(id),'
                         ' ep_id integer REFERENCES eps(id),'
                         ' filename varchar(511) unique,'
                         ' rating integer,'
                         ' year varchar(15),'
                         ' album varchar(255),'
                         ' title varchar(511));')

        self.cur.execute('CREATE TABLE IF NOT EXISTS song_moods ('
                         ' id integer auto_increment not null unique,'
                         ' mood_id integer REFERENCES moods(id),'
                         ' song_id integer REFERENCES songs(id));')
        # self.cur.execute('ALTER TABLE `song_moods` ADD UNIQUE `unique_index`(`mood_id`, `song_id`);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS song_genres ('
                         ' id integer auto_increment not null unique,'
                         ' genre_id integer REFERENCES genres(id),'
                         ' song_id integer REFERENCES songs(id));')
        # self.cur.execute('ALTER TABLE `song_genres` ADD UNIQUE `unique_index`(`genre_id`, `song_id`);')

        self.cur.execute('CREATE TABLE IF NOT EXISTS song_artists ('
                         ' id integer auto_increment not null unique,'
                         ' artist_id integer REFERENCES artists(id),'
                         ' song_id integer REFERENCES songs(id));')
        # self.cur.execute('ALTER TABLE `song_artists` ADD UNIQUE `unique_index`(`artist_id`, `song_id`);')
        self.conn.commit()

    def insert_label(self, name):
        try:
            query = f"INSERT IGNORE INTO `labels`(`name`) VALUES (%s)"
            self.cur.execute(query, [name])
        except Exception as e:
            print(e, query, name)
            pass

    def insert_eps(self, label, cat_id, path):
        try:
            query = f"INSERT INTO `eps`(`label_id`, `catid`, `path`) VALUES ((select id from labels where name=%s), %s, %s);"
            self.cur.execute(query, (label, cat_id, path))
        except Exception as e:
            print(e, query, cat_id, path)
            pass

    def insert_mood(self, mood):
        try:
            query = f"INSERT IGNORE INTO `moods`(`name`) VALUES (%s);"
            self.cur.execute(query, [mood])
        except Exception as e:
            print(e, query, mood)
            pass

    def insert_genre(self, genre):
        try:
            query = f"INSERT IGNORE INTO `genres`(`name`) VALUES (%s);"
            self.cur.execute(query, [genre])
        except Exception as e:
            print(e, query, genre)
            pass

    def insert_artist(self, artist):
        try:
            query = f"INSERT IGNORE INTO  `artists`(`name`) VALUES (%s);"
            self.cur.execute(query, [artist])
        except Exception as e:
            print(e, query, artist)
            pass

    def insert_song(self, filename, label, ep, title, album, rating, year):
        try:
            query = f"INSERT INTO `songs`(`filename`, `label_id`, `ep_id`, `title`, `album`, `rating`, `year`) VALUES " \
                    f"(%s, " \
                    f"(select id from labels where name=%s limit 1), " \
                    f"(select id from eps where path=%s limit 1), " \
                    f"%s, " \
                    f"%s, " \
                    f"%s, " \
                    f"%s) " \
                    f"on duplicate key update " \
                    f"label_id=(select id from labels where name=%s limit 1), " \
                    f"ep_id=(select id from eps where path=%s limit 1), " \
                    f"title=%s, " \
                    f"album=%s, " \
                    f"rating=%s, " \
                    f"year=%s;"
            self.cur.execute(query, (filename, label, ep, title, album, rating, year, label, ep, title, album, rating, year))
        except Exception as e:
            print(e, query, (filename, label, ep, album, rating, year))
            pass

    def insert_song_mood(self, filename, mood):
        try:
            query = f"INSERT IGNORE INTO `song_moods`(`song_id`, `mood_id`) VALUES ((select id from songs where filename=%s), (select id from moods where name=%s));"
            self.cur.execute(query, (filename, mood))
        except Exception as e:
            print(e, query, mood)
            pass
    def insert_song_artist(self, filename, artist):
        try:
            query = f"INSERT IGNORE INTO `song_artists`(`song_id`, `artist_id`) VALUES ((select id from songs where filename=%s), (select id from artists where name=%s));"
            self.cur.execute(query, (filename, artist))
        except Exception as e:
            print(e, query, artist)
            pass
    def insert_song_genre(self, filename, genre):
        try:
            query = f"INSERT IGNORE INTO `song_genres`(`song_id`, `genre_id`) VALUES ((select id from songs where filename=%s), (select id from genres where name=%s));"
            self.cur.execute(query, (filename, genre))
        except Exception as e:
            print(e, query, genre)
            pass

    def done(self):
        self.conn.commit()

    def start(self):
        # Connect to MariaDB Platform
        try:
            self.conn = connect()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        # Get Cursor
        self.cur = self.conn.cursor()
