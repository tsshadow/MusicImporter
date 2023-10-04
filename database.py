# Module Imports
import mariadb
import sys
import os
from dotenv import load_dotenv


class Database:
    def __init__(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_DATABASE')
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = conn.cursor()
        self.create_table()


    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS labels ('
                         ' name varchar(255) not null unique,'
                         ' eps int);')
        self.cur.execute('DROP TABLE eps')
        self.cur.execute('CREATE TABLE IF NOT EXISTS eps ('
                         ' label varchar(255),'
                         ' catid varchar(255));')

    def insert_label(self, name, eps):
        conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_DATABASE')
        )
        cur = conn.cursor()
        cur.execute('INSERT INTO `labels`(`name`, `eps`) VALUES (\'' + name + '\',' + eps + ') ON DUPLICATE KEY UPDATE eps='+eps+';')
        conn.commit()

    def clear_eps(self):
        conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_DATABASE')
        )
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE `eps`;')
        conn.commit()

    def insert_eps(self, name, eps):
        conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_DATABASE')
        )
        cur = conn.cursor()
        cur.execute('INSERT INTO `eps`(`label`, `catid`) VALUES (\'' + name + '\',\'' + eps + '\');')
        conn.commit()


