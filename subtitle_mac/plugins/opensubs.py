__author__ = 'a.jha'

from .base_plugin import BasePlugin
import xmlrpclib
from .utility import get_hash, get_file
import zlib
import base64
import os
import codecs

SERVER = 'http://api.opensubtitles.org:80/xml-rpc'


class OpenSubs(BasePlugin):
    def __init__(self):
        self.movie_path = None
        self.normalized_path = None

    def download_sub(self, movie_path):
        self.movie_path = movie_path
        movie_hash = get_hash(self.movie_path)
        server = xmlrpclib.Server(SERVER)
        token = server.LogIn('abbi031892', 'submac123', 'en', 'sub_mac v0.1')['token']
        self.normalize_path()
        previous_find = -1
        for k in range(len(self.normalized_path.split('/')[-1].split(' ')) - 1, -1, -1):
            print 'Search trying for : '
            print ' '.join(self.normalized_path.split('/')[-1].split(' ')[:k + 1])
            response = server.SearchSubtitles(token, [
                {'query': ' '.join(self.normalized_path.split('/')[-1].split(' ')[:k + 1]), 'sublanguageid': 'eng'},
                {'moviehash': movie_hash}])
            if previous_find != -1 and (len(response['data']) > previous_find + 10):
                continue
            for data in response['data']:
                subtitle_id = data['IDSubtitleFile']
                subtitles = server.DownloadSubtitles(token, [subtitle_id])
                if len(subtitles['data']) > 1:
                    raise Exception('Unusual data length')
                data = base64.b64decode(subtitles['data'][0]['data'])
                decompressed_data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
                decompressed_data = decompressed_data.decode('utf-8', 'replace')
                _file = get_file(self.movie_path, decompressed_data)
                yield _file.name
            previous_find = len(response['data'])

    def normalize_path(self):
        if ' ' in self.movie_path:
            self.normalized_path = self.movie_path
        if '.' in self.movie_path:
            self.normalized_path = ' '.join(self.movie_path.split('.'))