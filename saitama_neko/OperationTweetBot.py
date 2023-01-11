"""
ファイル名 : OperationTweetBot.py
■概要
TwitterAPIを利用してツイートするモジュールです。
"""
import tweepy
# import SaitamaSeCats
# import CreateSentens
import TwittetAPICredentials

class OperationTweetBot():
    """
    Twitterクライアントを取り扱うクラス
    """
    def __init__(self):
        """
        処理
            外部からインポートした認証情報を利用してTwitterクライアントを初期化
        """
        self.credentials = TwittetAPICredentials.SaitamaCatInf()
        self.client = tweepy.Client(bearer_token = self.credentials.bearer_token, \
                                    consumer_key = self.credentials.consumer_key, \
                                    consumer_secret = self.credentials.consumer_secret, \
                                    access_token = self.credentials.access_token, \
                                    access_token_secret = self.credentials.access_secret)



def tweet(value):
    """
    処理
        "sci_client"で引数に指定された文字列をツイート
    引数
        ・value(string)
            ツイートしたい文字列
    """
    # OperationTweetBot.client.create_tweet(text = value)
    sci_client = OperationTweetBot()
    sci_client.client.create_tweet(text = value)

# 単体で実行したときの処理
if __name__ == '__main__':
    tweet('hoge')