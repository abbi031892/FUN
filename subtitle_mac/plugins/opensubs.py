__author__ = 'a.jha'

from .base_plugin import BasePlugin
import xmlrpclib
from .utility import get_hash
import zlib
import base64
import os


class OpenSubs(BasePlugin):
    def __init__(self):
        self.movie_path = None

    def download_sub(self, movie_path):
        self.movie_path = movie_path
        movie_hash = get_hash(self.movie_path)
        server_url = 'http://api.opensubtitles.org:80/xml-rpc'
        server = xmlrpclib.Server(server_url)
        token = server.LogIn('abbi031892', 'tunisana', 'en', 'sub_mac v0.1')['token']

        for k in range(len(self.movie_path.split('/')[-1].split(' ')) - 1, -1, -1):
            print 'Search trying for : '
            print ' '.join(self.movie_path.split('/')[-1].split(' ')[:k + 1])
            response = server.SearchSubtitles(token, [
                {'query': ' '.join(self.movie_path.split('/')[-1].split(' ')[:k + 1]), 'sublanguageid': 'eng'},
                {'moviehash': movie_hash}])
            for data in response['data']:
                subtitle_id = data['IDSubtitleFile']
                subtitles = server.DownloadSubtitles(token, [subtitle_id])
                if len(subtitles['data']) > 1:
                    raise Exception('Unusual data length')
                data = base64.b64decode(subtitles['data'][0]['data'])
                decompressed_data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
                base_folder = '/'.join(self.movie_path.split('/')[0:len(self.movie_path.split('/')) - 1])
                file_name = '.'.join(
                    self.movie_path.split('/')[-1].split('.')[0:len(self.movie_path.split('/')[-1].split('.'))-1])
                _file = open(os.path.join(base_folder, file_name + '.srt'), 'w+')
                _file.writelines(decompressed_data)
                yield _file.name