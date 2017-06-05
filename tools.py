import pickle
import json

import MeCab
import numpy as np


class TextTools:

    #MECAB_MODE=" -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd"
    #MECAB_MODE = '-d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd/'
    #tagger = MeCab.Tagger(MECAB_MODE)
    #tagger.parse("")
    @classmethod
    def parse(cls, text):
        u"""記号を取り除きスペース区切りでテキストを返す
        入力：str
        返値：str
        """
        node = cls.tagger.parseToNode(text).next
        result=""
        while node:
            word=node.surface
            print(word,word.isalpha())
            #if word.isalpha() or "/" in word or "%" in word or "[]" in word or "「" in word or "」" in word:
            #    node = node.next
            #    continue
            word = node.surface
            node = node.next
            result += word + " "
        return result

    @classmethod
    def conect_timeline(cls, timeline):
        """ツイートのリストを一つの文字列にして返す
        """
        format_text = ""
        for tweet in timeline:
            if "http" in tweet["text"]:
                continue
            split_text = tweet["text"].rsplit()
            for sentence in split_text:
                if sentence[0] != "@":
                    format_text += sentence + "。"
        return format_text

    @classmethod
    def make_dataset(cls, tweet_path, vocab):
        """データ・セットを作る
        引数：対象のタイムラインとそのボキャブラリー
        返値：データセットと
        """
        text = cls.conect_timeline(pickle.load(open(tweet_path, "rb")))
        node = cls.tagger.parseToNode(text)
        result=[]
        while node:
            word = node.surface
            feature = node.feature.split(',')
            node = node.next
            if word:
                if word not in vocab:
                    vocab[word] = (len(vocab), feature)
                result.append(word)

        dataset = np.array([vocab[word][0] for word in result], dtype=np.int32)
        print ('corpus length:{} vocab size:{}'.format(len(result), len(vocab)))
        return (dataset, result, vocab)
    """
    def get_twit_list(self, exclude_rep=0, include_rt=0, count=200, max_id=None, since_id=None):
        req = self.get_twit(exclude_rep, include_rt, count=200, max_id=None, since_id=None):
        if req is None:
            return []
        return [{x: twit[x] for x in twit
                 if x == "text"or x == "id_str" or x == "created_at"}
                for twit in req]

    def save_timeline(self, save=1, rep=0):
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
            new_timeline = self.get_twit_list(contain_rep=rep, max_id=max_id, since_id=since_id)
            if api_use_count > 1:
                new_timeline = new_timeline[1:]
            if len(new_timeline) <= 0:
                break
            twit_count += len(new_timeline)
            max_id = new_timeline[-1]["id_str"]
            timeline += new_timeline
        timeline += old_timeline
        if twit_count and save:
            json.dump(timeline, open(self.data_path, "w"), sort_keys=True, indent=4)
        print("added:{} tweet  api: {} used".format(twit_count, api_use_count))
        return api_use_count
    """

def test():
    text = u"高椅くんは、勉強しなかったので、点数がとれず、悔しがっていたのをいま思い出すと、残念だ。"
    return TextTools.parse(text)
