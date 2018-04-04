# Alexander Ross (asr3bj), Analyser_Subclasses.py
# this was created Apr, 2018

import re
from sentiment.Analyser_Base import AnalyserBase
from textblob import TextBlob
from vaderSentiment import vaderSentiment


class StandardAnalysis(AnalyserBase):
    """this is the standard analysis which will consist of a textblob analysis"""
    def __init__(self):
        pass

    def check(self, msg):
        vs = self.analyse(msg)
        if vs >= 0.1:
            if vs > 0:
                return True
        if vs <= -0.1:
            if vs <= 0:
                return False
        else:
            return None

    def analyse(self, msg):
        return TextBlob(msg.text).sentiment.polarity

class VaderAnalysis(AnalyserBase):
    def __init__(self):
        self.analyser = vaderSentiment.SentimentIntensityAnalyzer()

    def check(self, msg):
        vs = self.analyser.polarity_scores(msg.text)
        if self.rules(msg):
            return None
        if not vs['neg'] > 0.005:
            if vs['pos'] - vs['neg'] > 0:
                return True
        if not vs['pos'] > 0.005:
            if vs['pos'] - vs['neg'] <= 0:
                return False
        return None

    @staticmethod
    def rules(msg):
        if msg.user == "GroupMe":
            return True
        if msg.text == "attachment only":
            return True
        if re.match("(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",
                    msg.text) is not None:
            return True
        return False