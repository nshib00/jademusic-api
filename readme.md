# JadeMusic API


![Static Badge](https://img.shields.io/badge/made%20by-nshib00-%236dedad)
![Static Badge](https://img.shields.io/badge/API%20version-1.0-orange)
![Static Badge](https://img.shields.io/badge/python-3.11.4-blue)
![Static Badge](https://img.shields.io/badge/djangorestframework-3.14-cyan)
![Static Badge](https://img.shields.io/badge/python-100%25-green)


---

## Description

API for __searching__ and __downloading__ music from site [Hitmo](https://rur.hitmotop.com/) and its mirrors.<br>
It allows you to parse the site and download __many tracks in one request__ instead of manually downloading each track and wasting a lot of time on it.

---

## Also about the project

JadeMusic API written in _Python_ using _Django REST Framework_.

This API is used by another my project - [JadeMusic](https://github.com/nshib00/jademusic-bot) Telegram bot.

---

## With JadeMusic API you can download:
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
  

    