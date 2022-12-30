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
    CONSUMER_KEY = 'OGoft9gEziejXsRQ2QWtm6h5c'
    CONSUMER_SECRET = 'Qlo3CeL5kTsnoRFxY7TtcXrCLEDIzknEUr35i32vTHYOQmFMRI'
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKOTkwEAAAAAfWN%2FrZBAGdqlSVr7Sx5PmlBSxJ4%3DRwQy8lc1ENSx5rSvPqBwkZGDprgj6U2RIrsVVEVz6RYvyPkqPe'
    ACCESS_TOKEN = '1608356963527843843-fFW4ZWNQ4GxClmWEaGBmecMWsUriu6'
    ACCESS_SECRET = 'dPdDEK8Rjh1y2lbWyP8ZMUNqTWAEeMxc2oBgrZO1MgxeL'
    OperationTweetBot(CONSUMER_KEY,CONSUMER_SECRET,BEARER_TOKEN,ACCESS_TOKEN,ACCESS_SECRET).tweet(SaitamaSeCats.CreateSentens('s').sentens_2())