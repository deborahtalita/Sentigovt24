from django.shortcuts import render
from sentiment.crawl import crawl_tweet
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet

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