# Alexander Ross (asr3bj), analysis.py
# this was created Mar, 2018

import GroupMe_Interface.retrieve_groups as retrieve_groups
from tqdm import tqdm
from sentiment.stat_object import stat_object, run
from sentiment.Analyser_Subclasses import StandardAnalysis, VaderAnalysis, SplitSentenceAnalysis


def all_sentiments(groups, method):
    """pos_msgs, neg_msgs, stats = [], [], [] """
    stats = []
    for group in tqdm(groups):
        stat = stat_object(group)
        for msg in group.messages:
            check = method.check(msg)
            if check is None: continue
            if check:
                stat.pos_count += 1
                stat.pos_msgs = msg
            #    pos_msgs.append(msg)  # remember to delete these and return only stats
            if not check:
                stat.neg_count += 1
                stat.neg_msgs = msg
             #   neg_msgs.append(msg)  # remember to delete these and return only stats
        stats.append(stat)
    return stats


def critical(msgs):
    pass
# running analysis


retrieve_groups.retrieve_all()
stat_l1 = all_sentiments(retrieve_groups.cache_groups,SplitSentenceAnalysis())
stat_l2 = all_sentiments(retrieve_groups.cache_groups, StandardAnalysis())

for i in range(len(stat_l1)):
    stat_l2[i].compare(stat_l1[i])
run()

"""
write(p_msgs, "pos_msgs.txt")
write(n_msgs, "neg_msgs.txt")
write(p_msgs_t, "pos_msgs_t.txt")
write(n_msgs_t, "neg_msgs_t.txt")
"""
