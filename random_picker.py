from twitter import Twitter, User
import time
import os
import random
import json
import CCAA


def random_picker(ids=CCAA.target, path="data/excahnge.json"):
    target = User(ids)
    exchange_list = target.follow_exchanger()
    random.shuffle(exchange_list)
    pick = exchange_list.copy()
    for _ in range(10):
        user = User(random.sample(set(pick), 1)[0])
        user_info = user.user_info()
        if user_info is not None:
            ids, name = user_info["id"], user_info["name"]
            print(name)
            pick += user.follow_exchanger()
    random.shuffle(pick)
    for ids in pick[:50]:
        print("get ", ids, "'s tweet")
        user = User(ids)
        if not Twitter.api_use_start:
            Twitter.api_use_start = time.time()
        user.save_timeline()
        if Twitter.api_use_count >= 150:
            sleep_time = max(0, 900 - (time.time() - Twitter.api_use_start))
            print("limit!! sleep : ", sleep_time, "s")
            time.sleep(sleep_time)
            Twitter.api_use_start = None
            Twitter.api_use_count = 0


if __name__ == "__main__":
    random_picker()
