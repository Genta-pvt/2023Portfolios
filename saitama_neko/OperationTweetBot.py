import tweepy
import SaitamaSeCats
import CreateSentens
import TwCredentials


# ツイートするクラス
class OperationTweetBot():
    def __init__(self):
        self.credentials = TwCredentials.SaitamaCatInf()
        self.client = tweepy.Client(bearer_token = self.credentials.bearer_token, \
                                    consumer_key = self.credentials.consumer_key, \
                                    consumer_secret = self.credentials.consumer_secret, \
                                    access_token = self.credentials.access_token, \
                                    access_token_secret = self.credentials.access_secret)

    
def tweet(value):
    # OperationTweetBot.client.create_tweet(text = value)
    sci_client = OperationTweetBot()
    sci_client.client.create_tweet(text = value)

# 単体で実行したときの処理
if __name__ == '__main__':
    tweet('hoge')