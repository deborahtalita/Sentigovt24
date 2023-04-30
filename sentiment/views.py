from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from sentiment.crawl import crawl_tweet, MyStreamListener
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet, Bacapres
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

def bacapres_list(request):
    bacapres = Bacapres.objects.all()
    data = {}
    data['object_list'] = bacapres
    return render(request, 'create_bacapres.html', data)

def create_bacapres(request):
    bacapres = Bacapres.objects.all()
    data = {}
    data['object_list'] = bacapres
    form = bacapres_form.BacapresForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Bacapres was succesfully added!'))
        else:
            messages.error(request, 'Error saving form')
    data['form'] = form
    return render(request, 'create_bacapres.html',data)

def edit_bacapres(request, id):
    context = {}
    bacapres = get_object_or_404(Bacapres,id=id)
    form = bacapres_form.BacapresForm(request.POST or None, instance=bacapres)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('sentiment:create_bacapres'))
    context['form'] = form
    return render(request,'create_bacapres.html', context)
