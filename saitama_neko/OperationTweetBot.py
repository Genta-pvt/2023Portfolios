import tweepy
import SaitamaSeCats



# ツイートするクラス
class OperationTweetBot():
    def __init__(self,consumer_key,consumer_secret,bearer_token,access_token,access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = bearer_token
        self.access_token = access_token
        self.access_secret = access_secret
        self.client = tweepy.Client(bearer_token = self.bearer_token, consumer_key = self.consumer_key, consumer_secret = self.consumer_secret, access_token = self.access_token, access_token_secret = self.access_secret)

    
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
    OperationTweetBot(CONSUMER_KEY,CONSUMER_SECRET,BEARER_TOKEN,ACCESS_TOKEN,ACCESS_SECRET).tweet(SaitamaSeCats.CreateSentens('s').sentens_2())