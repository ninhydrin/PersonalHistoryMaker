import twitter
import time
import os
import random
import json
import CCAA


def random_picker(ids=CCAA.target, path="data/excahnge.json"):
    target = twitter.User(ids)
    if not os.path.exists(path):
        exchange_list = target.get_follow_exchanger()
        with open(path, "w") as f:
            save_ob = [{"id_str": i} for i in exchange_list]
            json.dump(save_ob, f, sort_keys=True, indent=4)
    else:
        with open(path) as f:
            id_json = json.load(f)
        exchange_list = [i["id_str"] for i in id_json]
    random.shuffle(exchange_list)
    pick = []
    for i in exchange_list[:8]:
        user = twitter.User(i)
        i = user.user_info()
        if i is not None:
            ids, name = i["id"], i["name"]
            print(name)
            pick += user.follow_exchanger()
    random.shuffle(pick)
    count = 0
    start_time = -1
    for ids in pick[:30]:
        print("get ", ids, "'s tweet")
        user = twitter.User(ids)
        if start_time == -1:
            count = 0
            start_time = time.time()
        num = user.save_timeline()
        count += num

        if count >= 150:
            sleep_time = 900 - (time.time() - start_time)
            if sleep_time < 0:
                sleep_time = 0
            print("limit!! sleep : ", sleep_time, "s")
            time.sleep(sleep_time)
            start_time = -1


if __name__ == "__main__":
    random_picker()
