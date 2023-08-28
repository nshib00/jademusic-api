# JadeMusic API


![Static Badge](https://img.shields.io/badge/made%20by-nshib00-%236dedad)
![Static Badge](https://img.shields.io/badge/API%20version-1.0-orange)
![Static Badge](https://img.shields.io/badge/python-3.11.4-blue)
![Static Badge](https://img.shields.io/badge/djangorestframework-3.14-cyan)

---

API for __searching__ and __downloading__ music from site [Hitmo](https://rur.hitmotop.com/) and its mirrors. 
This API is used by [JadeMusic](https://github.com/nshib00) Telegram bot.

JadeMusic API written in _Python_ using _Django REST Framework_.

---

## What is this API for?

 This API allows you to parse the site and download __many tracks in one request__ instead of manually downloading each track from the site and wasting a lot of time on it.

---

## With this API you can download:
  - Tracks:
     - By specific artist or track name
     - Popular tracks
     - New tracks
  - Popular albums
  - Playlists - tracks collected by genres, artists, time periods.

---

## API docs

Root API URL: (your host)/api/v1

API methods for searching and downloading tracks, albums and playlists described here.
- [Tracks](docs/tracks.md)
- [Albums](docs/albums.md)
- [Playlists](docs/playlists.md)
  

    