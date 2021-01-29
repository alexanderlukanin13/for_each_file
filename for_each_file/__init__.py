"""Top-level package for for-each-file."""

__author__ = """Alexander Lukanin"""
__email__ = 'alexander.lukanin.13@gmail.com'
__version__ = '0.1.0'

from ._for_each_file import (
    iter_files, iter_texts,  # noqa
    for_each_file, for_each_text,  # noqa
    iter_file_pairs, iter_text_pairs,  # noqa
    convert_files, convert_texts,  # noqa
    InvalidDirectoryError  # noqa
)
