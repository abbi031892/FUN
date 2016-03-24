__author__ = 'a.jha'

import argparse
import os
import hashlib
import requests


class Subtitle(object):
    def __init__(self, movie_path):
        self.movie_path = movie_path
        print(movie_path)

    def download_subs(self):
        movie_hash = self._get_hash()
        user_agent = self._get_user_agent()
        print movie_hash

    def _get_hash(self):
        readsize = 64 * 1024
        with open(self.movie_path, 'rb') as f:
            size = os.path.getsize(self.movie_path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def _get_user_agent(self):
        pass


def main():
    parser = argparse.ArgumentParser(description='Download subtitles')
    parser.add_argument('--p', dest='moviepath', type=str, required=True,
                        help='path of the movie with filename')

    args = parser.parse_args()
    Subtitle(args.moviepath).download_subs()


if __name__ == '__main__':
    main()