__author__ = 'a.jha'

from plugins.the_sub_db import DBSub
from plugins.opensubs import OpenSubs
import pysrt
from validate import Validate
from itertools import chain
import click
import os


class Subtitle(object):
    def __init__(self, movie_path, max_subs, validate):
        self.movie_path = movie_path
        self.validate = validate
        self.max_subs = max_subs

    def download_sub(self):
        print 'Validation: ' + str(self.validate)
        if self.validate:
            validate = Validate(self.movie_path)

        chain_iterators = chain(DBSub().download_sub(self.movie_path),
                                OpenSubs().download_sub(self.movie_path))

        for file_path in chain_iterators:
            if self.validate:
                subs = pysrt.open(file_path)
                text_slices = subs.slice(starts_after={'minutes': validate.start_min - 1, 'seconds': 59},
                                         ends_before={'minutes': validate.start_min,
                                                      'seconds': 11})
                text = ''
                for t_slice in text_slices.data:
                    text = text + t_slice.text + ' '
                text = ' '.join(text.split())
                print("For file : {} Movie Text is : {}".format(file_path, text))
                if validate.validate(text):
                    print("Found validated subtitle")
                    self._final(True)
                    return
                os.remove(file_path)
            else:
                continue
        self._final(False)

    @staticmethod
    def _final(result):
        if not result:
            print("Sorry", "We couldn't find a correct subtitle")
        else:
            print("Thanks for trying, your subtitle is inplace")


@click.command()
@click.option('--moviepath', default=None, help='File Path of the video')
@click.option('--validate', default=0, help="Whether you want validated subtitle downloaded, "
                                            "when it's true only one sub will be downloaded")
@click.option('--maxsubs', default=1, help='How many maximum subtitles you want to download')
def main(moviepath, validate, maxsubs):
    Subtitle(moviepath, maxsubs, validate).download_sub()


if __name__ == '__main__':
    main()