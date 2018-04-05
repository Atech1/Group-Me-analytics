# Alexander Ross (asr3bj), stats.py
# this was created Mar, 2018

mst = []
msn = []
from sentiment.Stat import Stat

class stat_object(object):
    """holds some stats"""
    def __init__(self, group):
        self.name = group.name
        self.group = group
        self.total = group.total
        self.members = len(group.members)
        self._p_count = 0
        self._n_count = 0
        self._p_msgs = []
        self._n_msgs = []

    @property
    def pos_count(self):
        return self._p_count

    @pos_count.setter
    def pos_count(self, value):
        self._p_count = value

    @property
    def neg_count(self):
        return self._n_count

    @neg_count.setter
    def neg_count(self, value):
        self._n_count = value

    @property
    def pos_msgs(self):
        return self._p_msgs

    @pos_msgs.setter
    def pos_msgs(self, value):
        self._p_msgs.append(value)

    @property
    def neg_msgs(self):
        return self._n_msgs

    @neg_msgs.setter
    def neg_msgs(self, value):
        self._n_msgs.append(value)

    def show(self):
        found = self.pos_count + self.neg_count
        if found == 0: found += 1
        pos_score_r, pos_score_abs = self.pos_count / (found),\
                                     self.pos_count/self.group.total
        neg_score_r, neg_score_abs = self.neg_count / (found),\
                                     self.neg_count/self.group.total
        percentage = round(100*(found)/(self.group.total), 4)
        print('\n')
        print("group: {}, members: {}".format(self.group.name, self.members))
        print("Positive: {}, Negative: {}, total found: {}, msg total: {}, percentage:{}%"
              .format(self.pos_count, self.neg_count, self.pos_count + self.neg_count, self.group.total, percentage))
        print("relative positive score: {}%, absolute positive score: {}%"
              .format(round(100*pos_score_r, 3), round(100*pos_score_abs, 3)))
        print("relative negative score: {}%, absolute negative score: {}%"
              .format(round(100*neg_score_r, 3), round(100*neg_score_abs, 3)))

    def compare(self, other):
        if self.name == other.name:
            print(self.name)
            found1 = self.neg_count + self.pos_count
            found2 = other.neg_count + other.pos_count
            if found1 == 0: found1 = 1
            if found2 == 0: found2 = 1
            print("percent classified: {}% compared to {}%"
                  .format(round(100*(self.neg_count + self.pos_count)/self.total, 3),
                                                    round(100*(other.neg_count + other.pos_count)/other.total, 3)))
            print("messages found: {}  compared to {}".format(self.neg_count + self.pos_count,
                                                              other.neg_count + other.pos_count))
            print("positive messages and %: tot: {}, {}%, compared to {}, {}%".format(self.pos_count,
                round(100*self.pos_count/found1, 3),other.pos_count, round(100*other.pos_count/found2, 3)))
            print("negative messages and %: tot: {}, {}% compared to {}, {}%".format(self.neg_count,
                100*round(self.neg_count/found1, 3),other.neg_count,100*round(other.neg_count/found2, 3)))
            print("loss: {}% compared to {}%".format(
                round(100*(self.total-(self.neg_count + self.pos_count))/self.total, 3),
                round(100*(other.total - (other.neg_count + other.pos_count))/other.total, 3)))
            self.compare_msgs(other)

    def compare_msgs(self, other):
        global mst, msn
        pos = [ msg.text for msg in self.pos_msgs if msg in other.pos_msgs]
        neg = [ msg.text for msg in self.neg_msgs if msg in other.neg_msgs]
        npos = [ msg.text for msg in self.pos_msgs if msg not in other.pos_msgs]
        nneg = [ msg.text for msg in self.neg_msgs if msg not in other.neg_msgs]
        mst = mst + [self.name, "pos messages"] + pos + ["neg messages"] + neg
        msn = msn + [self.name, "npos messages"] + npos + ["nneg messages"] + nneg
        return pos, neg   # I don't know about this

    def stats(self):
        found = self.pos_count + self.neg_count if self.pos_count + self.neg_count > 0 else 1
        pos_score_r, pos_score_abs = round(100*self.pos_count / (found), 3),\
                                     round(100*self.pos_count / self.group.total, 3)
        neg_score_r, neg_score_abs = round(100*self.neg_count / (found), 3),\
                                     round(100*self.neg_count / self.group.total, 3)
        total_percentage = round(100 * (found) / (self.group.total), 4)
        return Stat(self.total, found, total_percentage, pos_score_r, neg_score_r, pos_score_abs, neg_score_abs, self.members)

def write(lst, file_name):
    with open(file_name, "w", encoding = "utf-8") as f:
        for msg in lst:
            f.write("{}".format(msg) + '\n')
        f.close()

def run():
    write(mst, "Union Messages.txt")
    write(msn, "no Match.txt")