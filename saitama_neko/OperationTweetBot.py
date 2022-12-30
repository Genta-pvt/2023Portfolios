import tweepy
import SaitamaSeCats
import TwCredentials


# ツイートするクラス
class OperationTweetBot():
    def __init__(self):
        # self.consumer_key = consumer_key
        # self.consumer_secret = consumer_secret
        # self.bearer_token = bearer_token
        # self.access_token = access_token
        # self.access_secret = access_secret
        self.credentials = TwCredentials.SaitamaCatInf()
        self.client = tweepy.Client(bearer_token = self.credentials.bearer_token, \
                                    consumer_key = self.credentials.consumer_key, \
                                    consumer_secret = self.credentials.consumer_secret, \
                                    access_token = self.credentials.access_token, \
                                    access_token_secret = self.credentials.access_token)

    
    def tweet(self,value):
        # self.api.update_status(SaitamaSeCats.CreateSentens('s').create_1())
        self.client.create_tweet(text = value)

# 単体で実行したときの処理
if __name__ == '__main__':
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    BEARER_TOKEN = ''
    ACCESS_TOKEN = ''
    ACCESS_SECRET = ''
    OperationTweetBot().tweet(SaitamaSeCats.CreateSentens('s').sentens_2())
    # print(Credentials.SaitamaCatInf().consumer_key)