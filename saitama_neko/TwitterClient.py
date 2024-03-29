"""
ファイル名 : OperationTweetBot.py
■概要
TwitterAPIを利用してツイートするモジュールです。
"""
import tweepy
import TwitterAPICredentials
from datetime import datetime


class TwitterClient:
    """
    Twitterクライアントを取り扱うクラス
    """

    def __init__(self):
        """
        処理
            認証情報を初期化
        """
        credentials = TwitterAPICredentials.SaitamaCatInf()
        self.bearer_token = credentials.cre_dict['bearer_token']
        self.consumer_key = credentials.cre_dict['consumer_key']
        self.consumer_secret = credentials.cre_dict['consumer_secret']
        self.access_token = credentials.cre_dict['access_token']
        self.access_token_secret = credentials.cre_dict['access_secret']

    def set_client(self):
        client = tweepy.Client(bearer_token=self.bearer_token,
                               consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token=self.access_token,
                               access_token_secret=self.access_token_secret)
        return client


def tweet(value):
    """
    処理
        "sci_client"で引数に指定された文字列をツイート
    引数
        ・value(string)
            ツイートしたい文字列
    """
    # OperationTweetBot.client.create_tweet(text = value)
    sci_client = TwitterClient().set_client()
    sci_client.create_tweet(text=value)
    print('Tweeted.')


def test_tweet():
    tw_body = '''
This is test tweet.
Execution date : {}
'''
    now_str = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    y_n = input('Do you want to run a test tweet? (y/n)')
    if y_n == 'y':
        try:
            tw_client = TwitterClient().set_client()
            tw_client.create_tweet(text=tw_body.format(now_str))
        except (tweepy.errors.Unauthorized, tweepy.errors.Forbidden) as e:
            print('====[Twitter API Error]====')
            print(e)
            print('===========================')
            y_n = input('Twitter client authentication failed.\nReset credential information? (y/n)')
            if y_n == 'y':
                credentials = TwitterAPICredentials.SaitamaCatInf()
                credentials.write_csv()
        else:
            print('Successfully tweeted!')


# 単体で実行したときの処理
if __name__ == '__main__':
    test_tweet()
