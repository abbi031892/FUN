__author__ = 'a.jha'

"""
Everything that can be re-used
"""
import os
import hashlib


def get_hash(movie_path):
    readsize = 64 * 1024
    with open(movie_path, 'rb') as f:
        size = os.path.getsize(movie_path)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()