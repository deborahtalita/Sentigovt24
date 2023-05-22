from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from sentiment.crawl import crawl_tweet, MyStreamListener
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet
from bacapres.models import Bacapres
from .forms.bacapres_form import BacapresForm
from django.contrib import messages
from django.views.generic import CreateView
from . import preprocessing
from .preprocessing import TextPreprocessing
from sentigovt2.decorators import role_required
from django.db.models import Count
import pickle
import joblib
import json
import pytz 
from django.core.paginator import Paginator
from datetime import datetime, timedelta

vectorizer = pickle.load(open("TFIDFvec.pickle","rb"))
classifier = joblib.load("MultinomialNBModel.joblib")

timezone = pytz.timezone('Asia/Jakarta')

def predict(text):
    test = []
    test.append(text)

    vect = vectorizer.transform(test)
    predicted = classifier.predict(vect)
    sentiment = ' '.join(predicted)
    
    return sentiment

def orderLabel(label):
    if label == '2-negative':
        return "negative"
    elif label == '1-neutral':
        return "neutral"
    elif label == '3-positive':
        return "positive"

@csrf_exempt
def crawl(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', None)
        data = crawl_tweet(query)

        result = []

        for i in range(0, len(data)):
            preprocessed = TextPreprocessing(data[i]['text'])
            preprocessed_text = preprocessed.preprocessed_text
            sentiment = predict(preprocessed_text)

            obj_tweet = Tweet(
                tweet_id = data[i]['tweet_id'],
                text = data[i]['text'],
                text_preprocessed = preprocessed_text,
                created_at = data[i]['created_at'],
                user_name = data[i]['user_name'],
                sentiment = orderLabel(sentiment),
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
        data = scrape_tweet()

        result = []

        for i in range(0, len(data)):
            preprocessed = TextPreprocessing(data[i]['text'])
            preprocessed_text = preprocessed.preprocessed_text
            sentiment = predict(preprocessed_text)

            obj_tweet = Tweet(
                tweet_id = data[i]['tweet_id'],
                text = data[i]['text'],
                text_preprocessed = preprocessed_text,
                created_at = data[i]['created_at'],
                user_name = data[i]['user_name'],
                sentiment = orderLabel(sentiment),
                bacapres = data[i]['bacapres']
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

def preprocess(request):
    text = "b'Kekuatan Politik Besar Bisa Tercipta Bila Prabowo Berpasangan dengan Erick Thohir di Pilpres 2024. KoalisiKebangsaa\xe2\x80\xa6 https://t.co/2k0all7i6r'"

    test = []
    preprocessed = TextPreprocessing(text=text)
    print(preprocessed.preprocessed_text)
    test.append(preprocessed.preprocessed_text)

    vect = vectorizer.transform(test)
    predicted = classifier.predict(vect)
    s = ' '.join(predicted)
    # Print List
    print(s)

def search(request):
    context = {}
    if request.method == 'POST':
        selected_options = request.POST.getlist('search_field')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        selected_options = [int(x) for x in selected_options[0].split(',')]
        start = datetime.strptime((datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')),('%Y-%m-%d'))
        end = datetime.strptime((datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')),('%Y-%m-%d'))

        start_date = start.replace(tzinfo=pytz.utc).astimezone(timezone)
        end_date = end.replace(tzinfo=pytz.utc).astimezone(timezone)
        # print(selected_options)
        # print(start_date.tzinfo)
        # print(end_date)

        # get tweet with a given date range
        tweet = Tweet.objects.filter(created_at__range=(start_date, end_date))

        # get bacapres
        bacapres = Bacapres.objects.filter(id__in=selected_options).order_by('id')
        # print(bacapres)
        context['bacapres'] = bacapres
        
        # get total tweet per bacapres
        bacapres_total_tweet = {}
        for res in bacapres:
            total_tweet = tweet.filter(bacapres=res.id).count()
            # print(total_tweet)
            bacapres_total_tweet[res.id] = total_tweet
        context['bacapres_total_tweet'] = bacapres_total_tweet

        # get tren total tweet per bacapres per day
        bacapres_total_tweet_per_day = {}
        cur_date = start_date
        for res in bacapres:
            bacapres_total_tweet_per_day[res.id] = []
            while cur_date <= end_date:
                # print(cur_date.strftime('%Y-%m-%d'))
                total_tweet_per_day = tweet.filter(bacapres=res.id).filter(created_at=cur_date).count()
                # print(total_tweet_per_day)
                bacapres_total_tweet_per_day[res.id].append(total_tweet_per_day)
                # print(bacapres_total_tweet_per_day[res.id])
                cur_date += timedelta(days=1)
        context['bacapres_total_tweet_per_day'] = bacapres_total_tweet_per_day

        # get total tweet per classification
        total_sentiment = {}
        for res in bacapres:
            tokoh_tweets = tweet.filter(bacapres=res.id)
            neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
            total_sentiment[res.id] = {'neg_sentiment':neg_sentiment}
            pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
            total_sentiment[res.id].update({'pos_sentiment':neg_sentiment})
            neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
            total_sentiment[res.id].update({'neu_sentiment':neu_sentiment})
            print(total_sentiment[res.id])
        context['total_sentiment'] = total_sentiment
    
        # get tweet list per bacapres
        selected_bacapres = request.GET.get('bacapres')
        tokoh_tweets = tweet.filter(bacapres=bacapres).order_by('-created_at')
        paginator = Paginator(tokoh_tweets, 10)  # 10 items per page
        page_number = request.GET.get('page')  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

    context['title'] = 'Manual Search'
    context['active_page'] = 'dashboard'
    return render(request, 'dashboard.html', context)