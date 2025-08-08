
# 🎵 Music Importer – Overview

**Music Importer** is a Python application designed to fully automate the process of organizing newly downloaded music files. It handles everything from downloading to tagging and archiving, with support for multiple sources such as YouTube, SoundCloud, and manual rar files.

Whether you're a DJ, a collector, or just someone with a messy `Downloads` folder, Music Importer helps keep your library clean, structured, and fully tagged — with minimal manual intervention.

Music importer is a personal project which means that it does not have a generic setup. 
---

## 🚀 What Does It Do?

Music Importer automates the following tasks:

1. **Download**

   * Automatically downloads music from supported platforms:

     * 🎧 **YouTube**: channel/playlist-based music grabbing
     * 🎧 **SoundCloud**: artist/track-based downloading with throttle management
     * 📁 **Manual downloads**: handles ZIPs/RARs from sites like 1gabba
   * Download steps accept an optional `breakOnExisting` flag to stop early when an item is already archived.

2. **Unpack**

   * Extracts and cleans up `.zip` / `.rar` archives (especially from 1gabba)
   * Flattens nested folders
   * Normalizes file and folder names

3. **Tag**

   * Automatically fills in MP3/FLAC/M4A tags like:

     * Title
     * Artist
     * Genre
     * Year
     * BPM
   * Detects track length (songs vs. livesets)
   * Runs smart rules for guessing missing info from file names or folder structures
   * Supports custom remixer/genre/label databases

4. **Move**

   * Organizes tagged files into a clean folder structure based on genre, artist, or source
   * Prevents duplicates and supports overwriting, merging, or archiving

5. **Archive**

   * Keeps track of previously imported files (YouTube/SoundCloud archive)
   * Supports database-based archive tracking (no need for `--download-archive` text files)

---

## 🛠 Example Workflow

1. You manually or automatically download a ZIP from 1gabba.
2. Music Importer detects the new archive and unpacks it.
3. It scans the unpacked files, identifies the artist/track/title.
4. It looks up additional info (e.g. BPM, genre) or guesses it smartly.
5. It tags the music files and moves them to your collection.
6. If downloaded from YouTube/SoundCloud, the tool adds them to its archive database.

---

## 🔧 Built With

* Python 3
* `yt-dlp` for downloading
* `mutagen` for audio tagging
* `librosa` for BPM detection
* MariaDB or SQLite for archiving and tag metadata

---

## 🔐 Security

The API restricts cross‑origin requests to trusted origins through CORS middleware.
For production deployments you should place the service behind a reverse proxy such as
Nginx and enable HTTP Basic Authentication.

Optionally, set the `API_KEY` environment variable to require clients to include the
key via the `X-API-Key` header (REST) or `api_key` query parameter (WebSocket).

---



## 👨‍💻 Who Is It For?

* Personal project, specifically tailored for my needs
