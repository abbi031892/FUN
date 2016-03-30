__author__ = 'a.jha'

import os
import subprocess
import speech_recognition as sr
from fuzzywuzzy import fuzz

WIT_AI_KEY = "77EWVGGFQHHZZFOJY3HG732X56K6NMSM"
GOOGLE_KEY = "AIzaSyBUYmoOGm2i5OYdvikRQUfM0U58Cpz869o"
API_AI_CLIENT_ACCESS_TOKEN = "23d5c8cbcd254e36ad693397d93cc7be"
API_AI_SUBSCRIPTION_KEY = "0200c1f1-f0bc-4251-b33e-23429dda35da"


class Validate(object):
    def __init__(self, movie_path):
        self.movie_path = movie_path
        self.r = sr.Recognizer()
        self.audio = None
        self.start_min = None
        self.movie_texts = self._get_movie_texts()
        print("Minute chosen is : " + str(self.start_min))
        print("Decided movies texts are : " + ' #_# '.join(self.movie_texts))
        
    def validate(self, sub_text):
        if not self.movie_texts or not sub_text:
            return False
        for data_text in self.movie_texts:
            if fuzz.ratio(data_text, sub_text) > 50:
                return True
        return False

    def _set_audio(self):
        try:
            with sr.WavFile(self.converted_wav) as source:
                self.audio = self.r.record(source)
        except Exception as e:
            self.audio = None
            print e.message
            print "BAD FILE"

    def _set__mp4_clip_path(self, start_time, end_time):
        self.converted_mp4 = os.path.join(os.path.dirname(self.movie_path), 'small.mp4')
        with open(self.converted_mp4, 'w+'):
            copy_comm = "ffmpeg -y -i '{}' -ss {} -c copy -to {} '{}'".format(self.movie_path, start_time.strip(),
                                                                              end_time.strip(), self.converted_mp4)
            print copy_comm
            subprocess.check_call(copy_comm, shell=True)

    def _set_wav_clip_path(self):
        self.converted_wav = os.path.join(os.path.dirname(self.movie_path), 'small.wav')
        with open(self.converted_wav, 'w+'):
            to_wav_comm = "ffmpeg -y -i '{}' -map 0:1 -acodec pcm_s16le -ac 2 '{}'".format(self.converted_mp4, self.converted_wav)
            print to_wav_comm
            subprocess.call(to_wav_comm, shell=True)

    def _set_clip_path(self, start_time, end_time):
        self._set__mp4_clip_path(start_time, end_time)
        self._set_wav_clip_path()

    def _get_movie_texts(self):
        wit_text = ''
        google_text = ''
        api_ai_text = ''
        self.start_min = 9
        while not wit_text or not google_text or not api_ai_text:
            self.start_min += 1
            self._set_clip_path('00:' + str(self.start_min) + ':00.000', '00:' + str(self.start_min) + ':10.000')
            self._set_audio()
            if not self.audio:
                continue
            try:
                wit_text = self.r.recognize_wit(self.audio, key=WIT_AI_KEY)
                google_text = self.r.recognize_google(self.audio, key=GOOGLE_KEY)
                api_ai_text = self.r.recognize_api(self.audio, username=API_AI_CLIENT_ACCESS_TOKEN,
                                                   password=API_AI_SUBSCRIPTION_KEY)
            except sr.UnknownValueError:
                print("Wit.ai could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Wit.ai service; {0}".format(e))
            except Exception:
                pass

        self.audio = None
        os.remove(self.converted_mp4)
        os.remove(self.converted_wav)
        return [wit_text, google_text, api_ai_text]