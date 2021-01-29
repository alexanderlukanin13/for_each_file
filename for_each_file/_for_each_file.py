"""
This module contains for_each_file implementation.
"""

import os
from pathlib import Path
from typing import Callable, Iterable, Tuple, Union, Any


class InvalidDirectoryError(Exception):
    pass


def _ensure_dir(dir_path, must_exist=True):
    dir_path = Path(dir_path)
    s = str(dir_path)
    if '*' in s or '?' in s:
        raise InvalidDirectoryError(f'Path contains invalid symbols: {dir_path}')
    if dir_path.exists():
        if not dir_path.is_dir():
            raise NotADirectoryError(f'Not a directory: {dir_path}')
    elif must_exist:
        raise FileNotFoundError(f'Directory not found: {dir_path}')
    return dir_path


def iter_files(dir_path: Union[str, Path], pattern: str = '**/*') -> Iterable[Path]:
    dir_path = _ensure_dir(dir_path)
    # NOTE: we must do list() to take a "snapshot" of all files at a given moment.
    # This is to ensure predictable behavior.
    for file_path in list(dir_path.glob(pattern)):
        if not file_path.is_file():
            continue
        yield file_path


def iter_texts(dir_path: Union[str, Path], pattern: str = '**/*', encoding=None, errors=None) -> Iterable[str]:
    for file_path in iter_files(dir_path, pattern):
        yield file_path.read_text(encoding=encoding, errors=errors)


def for_each_file(dir_path: Union[str, Path], function: Callable[[Path], Any], pattern: str = '**/*') -> None:
    for file_path in iter_files(dir_path, pattern):
        function(file_path)


def for_each_text(dir_path: Union[str, Path], function: Callable[[str], Any], pattern: str = '**/*', encoding=None, errors=None) -> None:
    for file_path in iter_texts(dir_path, pattern, encoding, errors):
        function(file_path)


def iter_file_pairs(source_dir: Union[str, Path], target_dir: Union[str, Path], pattern: str = '**/*') -> Iterable[Tuple[Path, Path]]:
    # Make sure caller is not messing up the directory structure.
    source_dir = _ensure_dir(source_dir)
    target_dir = _ensure_dir(target_dir, must_exist=False)
    if target_dir in source_dir.parents or source_dir in target_dir.parents:
        raise InvalidDirectoryError('Source must not be a parent of Target (and vice versa)')

    parents = set()  # optimize os.makedirs for "thousands of files in a folder" scenario

    for source_file_path in iter_files(source_dir, pattern):
        target_file_path = target_dir / source_file_path.relative_to(source_dir)
        if target_file_path.parent not in parents:
            os.makedirs(target_file_path.parent, exist_ok=True)
            parents.add(target_file_path.parent)
        yield source_file_path, target_file_path


def convert_files(source_dir: Union[str, Path], target_dir: Union[str, Path], function: Callable[[Path, Path], Any], pattern: str = '**/*') -> None:
    for source_file_path, target_file_path in iter_file_pairs(source_dir, target_dir, pattern):
        function(source_file_path, target_file_path)


def iter_text_pairs(source_dir: Union[str, Path], target_dir: Union[str, Path], pattern: str = '**/*', encoding=None, errors=None) -> Iterable[Tuple[str, Path]]:
    for source_file_path, target_file_path in iter_file_pairs(source_dir, target_dir, pattern):
        yield source_file_path.read_text(encoding=encoding, errors=errors), target_file_path


def convert_texts(source_dir: Union[str, Path], target_dir: Union[str, Path], function: Callable[[str, Path], Any], pattern: str = '**/*', encoding=None, errors=None) -> None:
    for source_text, target_file_path in iter_text_pairs(source_dir, target_dir, pattern, encoding, errors):
        target_file_path.write_text(function(source_text), encoding=encoding, errors=errors)
