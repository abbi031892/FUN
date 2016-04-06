__author__ = 'a.jha'

"""
Everything that can be re-used
"""
import os
import hashlib
import codecs


def get_hash(movie_path):
    read_size = 64 * 1024
    with open(movie_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def get_file(movie_path, data):
    base_folder = '/'.join(movie_path.split('/')[0:len(movie_path.split('/')) - 1])
    file_name = '.'.join(
        movie_path.split('/')[-1].split('.')[0:len(movie_path.split('/')[-1].split('.')) - 1])
    start_index = 1
    changed_file_name = ''
    while os.path.isfile(os.path.join(base_folder, file_name + '.srt')):
        changed_file_name = file_name + str(start_index)
        start_index += 1
    _file = codecs.open(os.path.join(base_folder, changed_file_name + '.srt'), 'w+', 'utf-8')
    _file.write(data)
    return _file