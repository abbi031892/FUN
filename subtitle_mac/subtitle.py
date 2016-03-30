__author__ = 'a.jha'

import Tkinter
import tkFileDialog
import tkMessageBox
from plugins.the_sub_db import DBSub
import pysrt
from validate import Validate
from itertools import chain


class Subtitle(object):
    def __init__(self):
        self.movie_path = None

    def set_movie_path(self):
        root = Tkinter.Tk()
        root.withdraw()
        root.update()
        self.movie_path = tkFileDialog.askopenfilename()
        root.destroy()

    def download_sub(self):
        self.set_movie_path()
        validate = Validate(self.movie_path)
        # opensubs finder
        # SUBTITLE_REGEX = '\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d'

        chain_iterators = chain(DBSub().download_sub(self.movie_path))

        for file_path in chain_iterators:
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
                print("Found correct subtitle")
                self._final(True)
                return
            # os.remove(file_path)
        self._final(False)

    @staticmethod
    def _final(result):
        root = Tkinter.Tk()
        root.withdraw()
        root.update()
        if not result:
            tkMessageBox.showerror("Sorry", "We couldn't find a correct subtitle, although we left one there"
                                            " for you to try?")
        else:
            tkMessageBox.showinfo("Thanks for trying, your subtitle is inplace")
        root.destroy()


def main():
    Subtitle().download_sub()


if __name__ == '__main__':
    main()