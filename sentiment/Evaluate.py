# Alexander Ross (asr3bj), analysis.py
# this was created Mar, 2018

import GroupMe_Interface.retrieve_groups as retrieve_groups
from textblob import TextBlob
from tqdm import tqdm
from sentiment.stats import stat_object, run
from sentiment.Analyser_Base import AnalyserBase
from sentiment.Analyser_Subclasses import StandardAnalysis, VaderAnalysis

def split_into_sentences(text):
        return TextBlob(text).sentences

def all_sentiments(groups, method):
    pos_msgs, neg_msgs, stats = [], [], []
    for group in tqdm(groups):
        stat = stat_object(group)
        for msg in group.messages:
            if method.check is None: continue
            if method.check:
                stat.pos_count += 1
                stat.pos_msgs = msg
            if not method.check:
                stat.neg_count += 1
                stat.neg_msgs = msg
        stats.append(stat)
    return pos_msgs, neg_msgs, stats


def critical(msgs):
    pass
# running analysis


retrieve_groups.retrieve_all()
p_msgs, n_msgs, stat_l1 = all_sentiments(retrieve_groups.cache_groups,VaderAnalysis())
p_msgs_t, n_msgs_t, stat_l2 = all_sentiments(retrieve_groups.cache_groups, StandardAnalysis())

for i in range(len(stat_l1)):
    stat_l2[i].compare(stat_l1[i])
run()
"""
write(p_msgs, "pos_msgs.txt")
write(n_msgs, "neg_msgs.txt")
write(p_msgs_t, "pos_msgs_t.txt")
write(n_msgs_t, "neg_msgs_t.txt")
"""
