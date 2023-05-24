import time
import datetime
import pytz
import snscrape.modules.twitter as sntwitter
from dotenv import load_dotenv
from .models import Bacapres
load_dotenv()


# until_time = int(time.time())
# since_time = until_time - 3600
until_time = 1684505921
since_time = 1684831022
print(since_time, " ", until_time)

dt_utc = datetime.datetime.utcnow()
# print(dt_utc)
timezone = pytz.timezone('Asia/Jakarta')
# print(timezone)

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

def get_time(date):
    created_at = datetime.strftime(date)