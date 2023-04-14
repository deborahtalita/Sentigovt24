import snscrape.modules.twitter as sntwitter

def scrape_tweet(input_query, start_date, end_date):
    tweets = []
    limit= 50000

    for tweet in sntwitter.TwitterSearchScraper(input_query+' since:'+start_date+' until:'+end_date).get_items():
        if len(tweets) == limit:
            break
        else:
            tweet_id = str(tweet.id)
            data = {
            'tweet_id':tweet_id,
            'created_at':tweet.date,
            'user_name':tweet.user.username,
            'text':tweet.content,
            }
            print(tweet.id)
            tweets.append(data)
               

    return tweets