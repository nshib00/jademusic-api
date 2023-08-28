from pathlib import Path


def make_download_path() -> Path:
    download_path = Path('~').expanduser() / 'Downloads/JadeMusic'
    check_folder(download_path)
    return download_path


def check_track(track_path): # проверяет, скачан ли трек до запроса, чтобы избежать повторной загрузки уже скачанных треков
    if Path(track_path).is_file():
        return True
    return False


def check_folder(folder_path):
    if not Path(folder_path).is_dir():
        Path(folder_path).mkdir()


def change_download_path(new_path):
    check_folder(new_path)
    PathManager.download_path = Path(new_path)


class PathManager:
    download_path = make_download_path()


