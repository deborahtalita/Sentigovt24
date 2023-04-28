from django.shortcuts import render
from sentiment.crawl import crawl_tweet, MyStreamListener
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet
from .forms import bacapres_form
from django.contrib import messages
import tweepy

import json

@csrf_exempt
def crawl(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', None)
        data = crawl_tweet(query)

        result = []

        for i in range(0, len(data)):
            obj_tweet = Tweet(
                tweet_id = data[i]['tweet_id'],
                text = data[i]['text'],
                created_at = data[i]['created_at'],
                user_name = data[i]['user_name'],
            )

            result.append(obj_tweet)
        Tweet.objects.bulk_create(result)

        return JsonResponse({
            'code': 200, 
            'status': 'success',
            'data': []
        })
    return JsonResponse({
        'code': 404, 
        'status': 'not found',
        'data': []
    }) 

@csrf_exempt
def scrape(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', None)
        sd = data.get('start_date', None)
        ed = data.get('end_date', None)
        data = scrape_tweet(query,sd,ed)

        result = []

        for i in range(0, len(data)):
            obj_tweet = Tweet(
                tweet_id = data[i]['tweet_id'],
                text = data[i]['text'],
                created_at = data[i]['created_at'],
                user_name = data[i]['user_name'],
            )

            result.append(obj_tweet)
        Tweet.objects.bulk_create(result)

        return JsonResponse({
            'code': 200, 
            'status': 'success',
            'data': []
        })
    return JsonResponse({
        'code': 404, 
        'status': 'not found',
        'data': []
    })

def create_bacapres(request):
    context = {}
    form = bacapres_form.BacapresCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Bacpres was succesfully added!'))
        else:
            messages.error(request, 'Error saving form')
    context['form'] = form
    return render(request, 'create_bacapres.html',context)

@csrf_exempt
def stream(request):
    access_token = "3221004481-Vw4n4Wu5h1sbKT8jMx7ZreKR4vQIvrY8P1thkYu"
    access_token_secret = "pdsM9oOiUxZEUXrd3QkO1Trpi7gpApfXbqaCSP9kim3PL"
    api_key = "iXMeEq7FRzwDqTpXru578KeWJ"
    api_key_secret = "dbHcLVpyNuCmoGpIeuTFRuxqIz7WqllZkId9hSkiYB3OXhscfM"

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener,
                        tweet_mode="extended")
    myStream.filter(track=['ridwan kamil'])
    return JsonResponse({
            'code': 200, 
            'status': 'success',
            'data': []
    })