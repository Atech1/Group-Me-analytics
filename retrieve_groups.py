# Alexander Ross (asr3bj), retrieve_groups.py
# this was created Mar, 2018

import json
import requests
import datetime
import re
import settings
import time
import csv
from interface import Group

URL = settings.URL
Token = settings.Token
cache_groups = None

def get_response(response):
    """return json"""
    return response.json()['response']

def request(chat, param = None):
    if param is not None:
        return requests.get("{}/{}{}".format(URL, chat, Token), params = param)
    else:
        return requests.get("{}/{}{}".format(URL, chat, Token))

def get_groups():
    """finds all groups"""
    groups = []
    groupes = get_response(request('groups', {'per_page' : 100}))
    if groupes is not None:
        for group in groupes:
            print("ran group")
            groups.append(Group(group["group_id"], group["name"], group["members"],
                                count = group['messages']['count'], last_id = group['messages']['last_message_id']))
        return groups
    else:
        raise NotImplementedError

def groups_DM():
    groups = []
    groupes = get_response(request('chats', {'per_page': 100}))
    if groupes is not None:
        for group in groupes:
            print("running group")
            groups.append(Group(group['other_user']['id'], group['other_user']['name'],
                                [group['other_user']['name']],
                                'chats', group['messages_count'], last_id = group['last_message']['id']))
        return groups

def retrieve_all():
    global cache_groups
    groups = [] + groups_DM() + get_groups()
    cache_groups = groups
    return groups

def csv_write(file_name, groups = None): # remember to actually fix the issue with get_group() and group.members
    f = open(file_name, "w", encoding = "utf-8")
    csv.register_dialect('no_new_line', lineterminator = "\n")
    wr = csv.writer(f, dialect = "no_new_line")
    print('writing')
    wr.writerow(["Group", "Name", "Members"])
    for group in groups:
        wr.writerow([group.type, group.name, group.members])
        for msg in group.messages:
            wr.writerow([msg.user, msg.text, msg.favorites, msg.created])
        print('finished group')

csv_write("data_file.csv", retrieve_all())