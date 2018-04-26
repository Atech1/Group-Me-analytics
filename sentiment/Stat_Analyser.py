# Alexander Ross (asr3bj), Stat_Analyser.py
# this was created Apr, 2018

from sentiment.stat_object import stat_object

class Stat_Analyser(object):
    """this is a Analyser statistics object"""
    def __init__(self, stats):
        self.stat_groups = stats

    def compare_groups(self, other_analysers):  # this should compare self to all the other analyser
        pass

    def effectiveness_rating(self, limit):  # for groups larger than limit, what is the average return
        for stat in self.stat_groups:
            thing = stat.stats

    def representative_msgs(self, sample_size):  # this finds a bunch of representative msgs of sample size
        pass

    def show(self, limit = 400, sample_size = 10):
        print(self.effectiveness_rating(limit))
        print(self.representative_msgs(sample_size))