# Alexander Ross (asr3bj), Stat.py
# this was created Apr, 2018

class Stat(object):
    def __init__(self, total, found, rel, rel_pos, rel_neg, abs_pos, abs_neg, gmt ):
        self.total = total
        self.found = found
        self.tot_percentage = rel
        self.rel_pos_per = rel_pos
        self.rel_neg_per = rel_neg
        self.abs_pos_per = abs_pos
        self.abs_neg_per = abs_neg
        self.group_member_total = gmt

    def loss(self):
        return round(100 * (self.total - self.found)/self.total, 3)
