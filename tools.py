import pickle
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
        result = ""
        while node:
            word = node.surface
            print(word, word.isalpha())
            # if word.isalpha() or "/" in word or "%" in word or "[]" in word or "「" in word or "」" in word:
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
        result = []
        while node:
            word = node.surface
            feature = node.feature.split(',')
            node = node.next
            if word:
                if word not in vocab:
                    vocab[word] = (len(vocab), feature)
                result.append(word)

        dataset = np.array([vocab[word][0] for word in result], dtype=np.int32)
        print('corpus length:{} vocab:{}'.format(len(result), len(vocab)))
        return (dataset, result, vocab)


def test():
    text = u"高椅くんは、勉強しなかったので、点数がとれず、悔しがっていたのをいま思い出すと、残念だ。"
    return TextTools.parse(text)
