__author__ = 'a.jha'


class BasePlugin(object):
    def download_sub(self, movie_path):
        raise NotImplementedError