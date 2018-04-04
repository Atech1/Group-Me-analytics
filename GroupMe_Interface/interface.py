# Alexander Ross (asr3bj), interface.py
# this was created Mar, 2018
import json
import requests
import datetime
import re
import settings
URL = settings.URL
Token = settings.Token

def get_response(response):
    """return json"""
    return response.json()['response']


class Message(object):
    def __init__(self, msg_obj):
        self.id = int(msg_obj['id'])
        self.user_id = msg_obj['user_id']
        self.text = msg_obj['text']
        self.created = msg_obj['created_at']
        self.user = msg_obj['name']
        self.favorites = len(msg_obj['favorited_by'])
        if self.text is None:
            self.text = "attachment only"
        if self.text.startswith("b'") or self.user.startswith("b'"):
            self.text.encode("utf-8").strip()
            self.user.encode("utf-8").strip()




class Group(object):
    """
    this holds all of the data in a GroupMe group, such as the messages in it,
    the members of a group, and various statistics of the group.
    """

    def __init__(self, id_group, name, members, type = 'groups', count = 0, last_id = 0):
        self.group_id = id_group
        self.name = re.match(r"[^b']([^']*)[^']", name).group()
        self.type = type
        self.members = self.__process_members(members)
        self.total = count
        self.last_id = int(last_id)
        self.messages = [] + self.__collect_all_messages()
        self.most_liked = None

    def __process_members(self, members):
        if self.type is not "chats":
            mmbers = []
            for mem in members:
                mmbers.append(re.match(r"[^b']([^']*)[^']", mem['nickname']).group())
            return mmbers
        else:
            return [re.match(r"[^b']([^']*)[^']", mem).group() for mem in members]

    def get_messages(self, group_id, before_id = None):
        param = {'limit': 100}
        if before_id is not None:
            param['before_id'] = str(before_id)
        if self.type is not 'chats':
            msg = get_response(requests.get("{}/{}/{}/messages{}".format(URL, self.type ,group_id, Token)
                                            , params = param))
            return [Message(m) for m in msg['messages'] if m is not None and m['text'] is not None]
        else:
            param['other_user_id'] = group_id
            msg = get_response(requests.get(URL+"/direct_messages"+Token, params = param))
            return [Message(m) for m in msg['direct_messages'] if m is not None and 'text' in m]

    def __collect_all_messages(self, SinceT = None):
       # print(self.name)
        curCount = 0
        starting_id = self.last_id
        all_msgs = []
        while (curCount < self.total):
            starting_id += 1
            msgs = self.get_messages(self.group_id, starting_id)
            curCount += len(msgs)
            if SinceT is not None:
                all_msgs.extend([msg for msg in msgs if msg.created < SinceT])
            else:
                all_msgs.extend(msgs)
            starting_id = msgs[-1].id
        return all_msgs
