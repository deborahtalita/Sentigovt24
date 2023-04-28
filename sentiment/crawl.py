import time
import tweepy
from sentiment.models import Tweet

def crawl_tweet(input_query):
    access_token = "3221004481-Vw4n4Wu5h1sbKT8jMx7ZreKR4vQIvrY8P1thkYu"
    access_token_secret = "pdsM9oOiUxZEUXrd3QkO1Trpi7gpApfXbqaCSP9kim3PL"
    api_key = "iXMeEq7FRzwDqTpXru578KeWJ"
    api_key_secret = "dbHcLVpyNuCmoGpIeuTFRuxqIz7WqllZkId9hSkiYB3OXhscfM"

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # created_at = []
    # id = []
    # user_name = []
    # text = []
    crawlTweets = []

    for tweet in tweepy.Cursor(api.search_tweets,q=input_query,count=15,lang="id").items():
        # print(tweet.created_at, tweet.id,tweet.user.name,tweet.text)
        # created_at.append(tweet.created_at)
        # id.append(tweet.id)
        # user_name.append(tweet.user.name)
        # text.append(tweet.text.encode("utf-8"))
        # tweets = [tweet.created_at,tweet.id,tweet.user.name,tweet.text.encode("utf-8")]
        tweets = {
            'tweet_id':tweet.id,
            'created_at':tweet.created_at,
            'user_name':tweet.user.screen_name,
            'text':tweet.text.encode("utf-8"),
        }
        crawlTweets.append(tweets)
    

    return crawlTweets

class MyStreamListener(tweepy.Stream):
    
    def __init__(self, time_limit=300):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()
    
    def on_connect(self):
        print("Connected to Twitter API.")
        
    def on_status(self, status):
        
        res = {}
        # Tweet ID
        tweet_id = status.id
        
        # User ID
        user_id = status.user.id
        # Username
        username = status.user.name
        
        
        # Tweet
        if status.truncated == True:
            tweet = status.extended_tweet['full_text']
            hashtags = status.extended_tweet['entities']['hashtags']
        else:
            tweet = status.text
            hashtags = status.entities['hashtags']
        
        # Read hastags
        # hashtags = read_hashtags(hashtags)            
        
        # Retweet count
        # retweet_count = status.retweet_count
        # Language
        lang = status.lang
        
        print(status.text)
        # If tweet is not a retweet and tweet is in English
        # if not hasattr(status, "retweeted_status") and lang=="id":
            # Connect to database
            # dbConnect(user_id, username, tweet_id, tweet, retweet_count, hashtags)
            # tweet = {
            # 'tweet_id':status.id,
            # # 'created_at':status.created_at,
            # 'user_name':status.user.screen_name,
            # 'text':status.text.encode("utf-8"),
            # }
            # res.append(tweet)
            # Tweet.objects.bulk_create(res)
            
            
        if (time.time() - self.start_time) > self.limit:
            
            print(time.time(), self.start_time, self.limit)
            return False
            
    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False