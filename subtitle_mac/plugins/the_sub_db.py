__author__ = 'a.jha'

from utility import get_hash, get_file
import requests


class DBSub(object):
    def __init__(self):
        self.movie_path = None
        self.movie_hash = None
        self.user_agent = 'SubDB/1.0 (subtitle_mac/0.1; http://api.thesubdb.com/?action=languages)'

    def download_sub(self, movie_path):
        self.movie_path = movie_path
        movie_hash = get_hash(self.movie_path)
        headers = {'User-Agent': self.user_agent}
        response = requests.get('http://api.thesubdb.com/?action=search&hash={}'.format(movie_hash), headers=headers)
        if 'en' in response.text:
            subtitle = requests.get('http://api.thesubdb.com/?action=download&hash={}&language=en'.format(movie_hash),
                                    headers=headers)
            _file = get_file(self.movie_path, subtitle.text)
            yield _file.name