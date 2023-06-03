import time
import datetime
import pytz
import snscrape.modules.twitter as sntwitter
from .models import Bacapres, ScrapedTweet

until_time = int(time.time())
since_time = until_time - 7200
print(since_time, " ", until_time)

dt_utc = datetime.datetime.utcnow()
timezone = pytz.timezone('Asia/Jakarta')

def scrape_tweet():
    tweets = []
    bacapres = Bacapres.objects.all()
    print(bacapres)
    i = 1

    for query in bacapres:
        print(query.name)
        for tweet in sntwitter.TwitterSearchScraper(query.name+f" since_time:{since_time} until_time:{until_time}").get_items():
            tweet_date = tweet.date
            tweet_id = str(tweet.id)
            data = {
            'tweet_id':tweet_id,
            'created_at':tweet_date.replace(tzinfo=pytz.utc).astimezone(timezone),
            'user_name':tweet.user.username,
            'text':tweet.content,
            'bacapres':query.id,
            'keyword':query.name,
            }
            print(i)
            i=i+1
            tweets.append(data)

    return tweets

def getScrapedTweetDB():
    tweets = []
    i = 1
    scraped_tweet = ScrapedTweet.objects.filter(id__range=(102632,202632))

    for item in scraped_tweet:
        bacapres = item.bacapres
        data = {
            'tweet_id':item.tweet_id,
            'created_at':item.created_at,
            'user_name':item.user_name,
            'text':item.text,
            'bacapres':bacapres.id,
            'keyword':bacapres.keyword, 
        }
        print(i)
        i=i+1
        tweets.append(data)
    return tweets