# -*- coding: utf-8 -*-
import os
from requests_oauthlib import OAuth1Session
from requests.exceptions import ConnectionError, ReadTimeout#, SSLError
import json

import CCAA

target = CCAA.target


class Twitter:
    twitter_oauth = OAuth1Session(CCAA.CK, CCAA.CS, CCAA.AT, CCAA.AS)
    use = 0
    twit_url = "https://api.twitter.com/1.1/statuses/update.json"
    home_url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    # url = "https://api.twitter.com/1.1/frends/ids=%s.json"
    myFollower = "https://api.twitter.com/1.1/friends/list.json?count=200"
    statuses = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    favorites = "https://api.twitter.com/1.1/favorites/"

    friends = "https://api.twitter.com/1.1/friends/ids.json?"
    followes = "https://api.twitter.com/1.1/followers/ids.json?"

    users = "https://api.twitter.com/1.1/users/"
    stop_list = ("RT", "http")

    @classmethod
    def use_api(cls, num=1):
        cls.use += num

    @classmethod
    def __get_method(cls, url):
        try:
            req = cls.twitter_oauth.get(url)
        except ConnectionError as e:
            print("Connection Error ", e)
            return False
        except ReadTimeout as e:
            print("Read Timeout ", e)
            return False
        if req.status_code != 200:
            print("miss!!" + str(req.status_code))
            return False
        req = json.loads(req.text)
        return req

    @classmethod
    def word_search(cls, text):
        url = "https://api.twitter.com/1.1/search/tweets.json?q={}".format(text)
        req = cls.__get_method(url)
        return req

    @classmethod
    def twit_id(cls, ids):
        url = "https://api.twitter.com/1.1/statuses/show.json?id={}".format(ids)
        req = cls.__get_method(url)
        return req

    @classmethod
    def user_info(cls, ids, entity=False):
        url = cls.users+"show.json?user_id={}&include_entities={}".format(ids, entity)
        req = cls.__get_method(url)
        return req

    @classmethod
    def get_twit(cls, ids, exclude_rep=0, include_rt=0, count=200, max_id=None, since_id=None):
        url = cls.statuses + "user_id={}&count={}&exclude_replies={}&include_rts={}".format(ids, count, exclude_rep, include_rt)
        if max_id:
            url += "&max_id={}".format(max_id)  # max_id以下を取得
        if since_id:
            url += "&since_id={}".format(since_id)  # since_idより上を取得
        return cls.__get_method(url)

    @classmethod
    def get_follow_list(cls, target_id, to_string=True, count=5000):
        url = cls.friends
        query = "user_id={}&stringify_ids={}&count={}".format(
            target_id, to_string, count)
        url += query
        req = cls.__get_method(url)
        return req

    @classmethod
    def get_followe_list(cls, target_id, to_string=True, count=5000):
        url = cls.followes
        query = "user_id={}&stringify_ids={}&count={}".format(
            target_id, to_string, count)
        url += query
        req = cls.__get_method(url)
        return req

    @classmethod
    def twit_post(cls, content, ids=None):
        url = cls.twit_url
        params = {"status": content}
        if ids:
            url += "?in_reply_to_status_id="+ids
        req = cls.twitter_oauth.post(url, params=params)
        return req if req.status_code == 200 else False


class User:
    def __init__(self, target_id, data_dir="TimeLine"):
        self.target_id = target_id
        self.data_path = "{}/{}.json".format(data_dir, target_id)
        self.twitter = Twitter

    def user_info(self, entity=False):
        return self.twitter.user_info(self.target_id, entity)

    def follow_exchanger(self):
        follow = self.follow_list()
        follower = self.follower_list()
        if not follow or not follower:
            return []
        return list(set(follow["ids"]).intersection(set(follower["ids"])))

    def follow_list(self, to_string=True, count=5000):
        return self.twitter.get_follow_list(self.target_id, to_string, count)

    def follower_list(self, to_string=True, count=5000):
        return self.twitter.get_followe_list(self.target_id, to_string, count)

    def get_twit(self, exclude_rep=0, include_rt=0, count=200, max_id=None, since_id=None):
        return self.twitter.get_twit(self.target_id, exclude_rep, include_rt, count, max_id, since_id)

    def get_twit_list(self, exclude_rep=0, include_rt=0, count=200, max_id=None, since_id=None):

        req = self.get_twit(exclude_rep, include_rt, count, max_id, since_id)
        if not req:
            return []
        return [{x: twit[x] for x in twit
                 if x == "text"or x == "id_str" or x == "created_at"}
                for twit in req]

    def save_timeline(self):
        max_id = None
        twit_count = 0
        api_use_count = 0
        old_timeline = []
        timeline = []
        since_id = 0

        if os.path.exists(self.data_path):
            old_timeline = json.load(open(self.data_path))
            since_id = old_timeline[0]["id_str"]
        else:
            print("user id ", self.target_id, "is first")

        for i in range(40):
            api_use_count += 1
            new_timeline = self.get_twit_list(max_id=max_id, since_id=since_id)
            if api_use_count > 1:
                new_timeline = new_timeline[1:]
            if not new_timeline:
                break
            twit_count += len(new_timeline)
            max_id = new_timeline[-1]["id_str"]
            timeline += new_timeline
        timeline += old_timeline
        with open(self.data_path, "w") as f:
            json.dump(timeline, f, sort_keys=True, indent=4)
        print("added:{} tweet  api: {} used".format(twit_count, api_use_count))
        return api_use_count
