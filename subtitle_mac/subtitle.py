__author__ = 'a.jha'

import Tkinter
import tkFileDialog
import speech_recognition as sr
import tkMessageBox
import re
import subprocess
import os
from plugins.opensubs import OpenSubs
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pysrt
import srt


class Subtitle(object):
    def __init__(self):
        self.movie_path = None
        self.audio = None
        self.r = sr.Recognizer()

    def set_movie_path(self):
        root = Tkinter.Tk()
        root.withdraw()
        root.update()
        self.movie_path = tkFileDialog.askopenfilename()
        root.destroy()
        # Tkinter.Tk().deiconify()

    # def download_subs(self):
    #     movie_hash = self._get_hash()
    #     user_agent = self._get_user_agent()
    #     headers = {'User-Agent': user_agent}
    #     response = requests.get('http://api.thesubdb.com/?action=search&hash={}'.format(movie_hash), headers=headers)
    #     print movie_hash

    def download_sub(self):
        self.set_movie_path()
        # self.set_wav_path()
        # self.set_audio()
        # opensubs finder
        regex_pattern = '\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d'

        for file_path in OpenSubs().download_sub(self.movie_path):
            time_text = {}
            subs = pysrt.open(file_path)
            for subtitle in subs.data:
                time_text[str(subtitle.start) + ' --> ' + str(subtitle.end)] = subtitle.text_without_tags

            for time, text in time_text.iteritems():
                text = ' '.join(text.split())
                start_time = time.split(' --> ')[0].replace(",", ".")
                end_time = time.split(' --> ')[-1].replace(",", ".")
                # start_time = self.two_seconds_diff(start_time, ahead=False)
                # end_time = self.two_seconds_diff(end_time, ahead=True)
                print time, text, start_time, end_time
                self.set_wav_path(start_time, end_time)
                print 'test'
                self.set_audio()
                data_text = ''
                google_text = ''
                WIT_AI_KEY = "77EWVGGFQHHZZFOJY3HG732X56K6NMSM" # Wit.ai keys are 32-character uppercase alphanumeric strings
                try:
                    data_text = self.r.recognize_wit(self.audio, key=WIT_AI_KEY)
                    google_text = self.r.recognize_google(self.audio, key='AIzaSyBUYmoOGm2i5OYdvikRQUfM0U58Cpz869o')
                except sr.UnknownValueError:
                    print("Wit.ai could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Wit.ai service; {0}".format(e))
                except Exception as e:
                    print 'SAD'
                    continue
                print data_text + ' : ' + google_text + ' : ' + text
                if self.match([google_text, data_text], text):
                    print 'Fucking YES'
                    return
                else:
                    print 'SAD'
                    break

    # def _get_user_agent(self):
    #     return 'SubDB/1.0 (subtitle_mac/0.1; http://api.thesubdb.com/?action=languages)'

    def set_audio(self):
        try:
            with sr.WavFile(self.wav_path) as source:
                self.audio = self.r.record(source)
        except Exception as e:
            print e.message
            print "BAD FILE"

    def set_wav_path(self, start_time, end_time):
        self.mp4_path = os.path.join(os.path.dirname(self.movie_path), 'small.mp4')
        self.wav_path = os.path.join(os.path.dirname(self.movie_path), 'small.wav')
        with open(self.mp4_path, 'w+'):
            copy_comm = "ffmpeg -y -i '{}' -ss {} -c copy -to {} '{}'".format(self.movie_path, start_time.strip(),
                                                                              end_time.strip(), self.mp4_path)
            print copy_comm
            subprocess.check_call(copy_comm, shell=True)
        with open(self.wav_path, 'w+'):
            to_wav_comm = "ffmpeg -y -i '{}' -map 0:1 -acodec pcm_s16le -ac 2 '{}'".format(self.mp4_path, self.wav_path)
            print to_wav_comm
            subprocess.call(to_wav_comm, shell=True)

    @staticmethod
    def match(all_texts, text):
        if not all_texts or not text:
            return False
        for data_text in all_texts:
            if fuzz.ratio(data_text, text) > 50:
                return True
        return False

    def two_seconds_diff(self, time, ahead):
        splitted_time = time.split(':')
        if not ahead and int(splitted_time[2].split('.')[0]) >= 2:

            splitted_time[2] = str(int(splitted_time[2].split('.')[0]) - 2) + '.' + str(splitted_time[2].split('.')[1])
        elif int(splitted_time[2].split('.')[0]) < 58:
            splitted_time[2] = str(int(splitted_time[2].split('.')[0]) + 2) + '.' + str(splitted_time[2].split('.')[1])
        return ':'.join(splitted_time)



def main():
    Subtitle().download_sub()


if __name__ == '__main__':
    main()