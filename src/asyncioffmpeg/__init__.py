from __future__ import annotations
from pathlib import Path
import typing as T
import shutil
import functools


def get_videos(path: Path, suffixes: str | set[str] | None = None) -> T.Iterator[Path]:

    if not suffixes:
        suffixes = {".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov"}
    if isinstance(suffixes, str):
        suffixes = {suffixes}

    path = Path(path).expanduser()

    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a directory")

    return (f for f in path.iterdir() if f.is_file() and f.suffix in suffixes)


@functools.cache
def get_exe(name: str) -> str:
    if not (exe := shutil.which(name)):
        raise FileNotFoundError(name)
    return exe


def get_ffmpeg() -> str:
    return get_exe("ffmpeg")


def get_ffplay() -> str:
    return get_exe("ffplay")


def get_ffprobe() -> str:
    return get_exe("ffprobe")
