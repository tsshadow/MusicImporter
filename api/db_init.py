import logging
import os
import time

from pymysql import err as pymysql_errors

from postprocessing.Song.Helpers.DatabaseConnector import DatabaseConnector


# Static list of tables that should exist in the database.
REQUIRED_TABLES = [
    "soundcloud_accounts",
    "soundcloud_archive",
    "youtube_accounts",
    "youtube_archive",
    "artists",
    "artist_genre",
    "catid_label",
    "festival_data",
    "genres",
    "ignored_artists",
    "ignored_genres",
    "label_genre",
    "subgenre_genre",
]


MAX_ATTEMPTS = int(os.getenv("DB_INIT_MAX_RETRIES", "5"))
RETRY_DELAY = float(os.getenv("DB_INIT_RETRY_DELAY", "1"))


def _execute_with_retry(table: str, query: str) -> None:
    attempts = 0
    while attempts < max(1, MAX_ATTEMPTS):
        try:
            conn = DatabaseConnector().connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                conn.commit()
                return
            finally:
                conn.close()
        except (pymysql_errors.OperationalError, pymysql_errors.InterfaceError) as exc:
            attempts += 1
            logging.warning(
                "Failed to ensure table '%s' exists (attempt %s/%s): %s",
                table,
                attempts,
                max(1, MAX_ATTEMPTS),
                exc,
            )
            if attempts >= max(1, MAX_ATTEMPTS):
                break
            time.sleep(RETRY_DELAY * attempts)
        except Exception as exc:  # pragma: no cover - defensive
            logging.warning("Failed to ensure table '%s' exists: %s", table, exc)
            return

    logging.warning("Giving up on ensuring table '%s' exists after %s attempts.", table, max(1, MAX_ATTEMPTS))


def ensure_tables_exist() -> None:
    """Ensure required database tables exist."""
    table_queries = {
        "soundcloud_accounts": """
            CREATE TABLE IF NOT EXISTS soundcloud_accounts (
                name VARCHAR(255),
                soundcloud_id VARCHAR(255),
                PRIMARY KEY (name)
            )
        """,
        "soundcloud_archive": """
            CREATE TABLE IF NOT EXISTS soundcloud_archive (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account VARCHAR(255),
                video_id VARCHAR(255),
                filename TEXT,
                url TEXT,
                title TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX(account),
                INDEX(video_id)
            )
        """,
        "youtube_accounts": """
            CREATE TABLE IF NOT EXISTS youtube_accounts (
                name VARCHAR(255) PRIMARY KEY
            )
        """,
        "youtube_archive": """
            CREATE TABLE IF NOT EXISTS youtube_archive (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account VARCHAR(255),
                video_id VARCHAR(255),
                filename TEXT,
                url TEXT,
                title TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX(account),
                INDEX(video_id)
            )
        """,
        "artists": """
            CREATE TABLE IF NOT EXISTS artists (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                INDEX(name)
            )
        """,
        "artist_genre": """
            CREATE TABLE IF NOT EXISTS artist_genre (
                artist VARCHAR(255) NOT NULL,
                genre VARCHAR(255) NOT NULL,
                PRIMARY KEY (artist, genre)
            )
        """,
        "catid_label": """
            CREATE TABLE IF NOT EXISTS catid_label (
                catid VARCHAR(255) PRIMARY KEY,
                label VARCHAR(255) NOT NULL
            )
        """,
        "festival_data": """
            CREATE TABLE IF NOT EXISTS festival_data (
                festival VARCHAR(255) NOT NULL,
                year INT NOT NULL,
                date DATE NOT NULL,
                PRIMARY KEY (festival, year)
            )
        """,
        "genres": """
            CREATE TABLE IF NOT EXISTS genres (
                genre VARCHAR(255) NOT NULL,
                corrected_genre VARCHAR(255) NOT NULL,
                PRIMARY KEY (genre)
            )
        """,
        "ignored_artists": """
            CREATE TABLE IF NOT EXISTS ignored_artists (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                corrected_name VARCHAR(255),
                INDEX(name)
            )
        """,
        "ignored_genres": """
            CREATE TABLE IF NOT EXISTS ignored_genres (
                name VARCHAR(255) PRIMARY KEY,
                corrected_name VARCHAR(255)
            )
        """,
        "label_genre": """
            CREATE TABLE IF NOT EXISTS label_genre (
                label VARCHAR(255) NOT NULL,
                genre VARCHAR(255) NOT NULL,
                PRIMARY KEY (label, genre)
            )
        """,
        "subgenre_genre": """
            CREATE TABLE IF NOT EXISTS subgenre_genre (
                subgenre VARCHAR(255) NOT NULL,
                genre VARCHAR(255) NOT NULL,
                PRIMARY KEY (subgenre, genre)
            )
        """,
    }

    for table in REQUIRED_TABLES:
        query = table_queries[table]
        _execute_with_retry(table, query)
