import tweepy

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