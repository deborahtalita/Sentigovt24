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
# get times
dt_utc = datetime.utcnow()
timezone = pytz.timezone('Asia/Jakarta')
today = dt_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
seven_days_ago = today - timedelta(days=7)

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
    
def convertDate(date):
    date = datetime.strptime((datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')),('%Y-%m-%d'))
    date = date.replace(tzinfo=pytz.utc).astimezone(timezone)
    return date

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

        # assign query to session
        request.session['selected_options'] = selected_options
        request.session['selected_start_date'] = start
        request.session['selected_end_date'] = end

        # get tweet with a given date range
        # tweet = Tweet.objects.filter(created_at__range=(start_date, end_date))

        # get selected bacapres
        bacapres = Bacapres.objects.filter(id__in=selected_options).order_by('id')
        context['bacapres'] = bacapres
        if bacapres: context['active_item'] = bacapres.first()
        context['result'] = 'true'
        
#        #tweet list with pagination
        tokoh_tweets = Tweet.objects.filter(bacapres=11).order_by('-created_at')
        paginator = Paginator(tokoh_tweets, 10)  # 10 items per page
        page_number = request.GET.get('page')  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    else:
        # get bacapres

        options = request.session.get('selected_options')
        print("get_sessions",options)
        context       
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres_opt'] = bacapres 

    context['title'] = 'Manual Search'
    context['active_page'] = 'dashboard'
    return render(request, 'dashboard.html', context)

def getAllTotalTweet(request):
    context = {}

    dates = getDates()
    context['dates'] = dates

    # get bacapres
    if request.session.get('selected_options') != None:
        selected_options = request.session.get('selected_options')
        bacapres = Bacapres.objects.filter(id__in=selected_options).order_by('id')
    else:
        bacapres = Bacapres.objects.all().order_by('id')

    # get tweets
    if (request.session.get('selected_start_date') != None) and (request.session.get('selected_end_date') != None):
        start_date = convertDate(request.session.get('selected_start_date'))
        end_date = convertDate(request.session.get('selected_end_date'))
        tweet = Tweet.objects.filter(created_at__range=(start_date,end_date))
    else:
        tweet = Tweet.objects.filter(created_at__gte=seven_days_ago)

    # get tren total tweet per bacapres per day
    bacapres_total_tweet_per_day = []
    for res in bacapres:
        series_data = {'name':res.name,'data':[]}
        cur_date = seven_days_ago
        tokoh_tweets = tweet.filter(bacapres=res.id)
        while cur_date < today:
            date = cur_date.strftime('%Y-%m-%d')
            total_tweet_per_day = tokoh_tweets.filter(created_at=date).count()
            series_data['data'].append(total_tweet_per_day)
            cur_date += timedelta(days=1)
        bacapres_total_tweet_per_day.append(series_data)
    # print(bacapres_total_tweet_per_day)        
    context['bacapres_total_tweet_per_day'] = bacapres_total_tweet_per_day

    
    return JsonResponse(context)

def getDates():
    dates = []
    i = 0

    cur_date = seven_days_ago
    while cur_date < today:
        date = cur_date.strftime('%Y-%m-%d') 
        dates.append(date)
        cur_date += timedelta(days=1)

    return dates

def getAllTotalSentiment(request):
    context = {}

    dates = getDates()
    context['dates'] = dates

    # get bacapres
    if request.session.get('selected_options') != None:
        selected_options = request.session.get('selected_options')
        bacapres = Bacapres.objects.filter(id__in=selected_options).order_by('id')
    else:
        bacapres = Bacapres.objects.all().order_by('id')

    # get tweets
    if (request.session.get('selected_start_date') != None) and (request.session.get('selected_end_date') != None):
        start_date = convertDate(request.session.get('selected_start_date'))
        end_date = convertDate(request.session.get('selected_end_date'))
        tweet = Tweet.objects.filter(created_at__range=(start_date,end_date))
    else:
        tweet = Tweet.objects.filter(created_at__gte=seven_days_ago)
    
    # get total tweet per classification per day
    total_sentiment_per_day = {}
    for res in bacapres:
        total_sentiment_per_day[res.id] = []
        negative = {'name':'Negative', 'data':[]}
        positive = {'name':'Positive', 'data':[]}
        neutral = {'name':'Neutral', 'data':[]}

        cur_date = seven_days_ago
        while cur_date < today:
            date = cur_date.strftime('%Y-%m-%d')
            tokoh_tweets = tweet.filter(bacapres=res.id).filter(created_at=date)
            # print(date)

            neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
            # print("neg_sentiment",neg_sentiment)
            pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
            # print("pos_sentiment",pos_sentiment)
            neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
            # print("neu_sentiment",neu_sentiment)
            
            negative['data'].append(neg_sentiment)
            positive['data'].append(pos_sentiment)
            neutral['data'].append(neu_sentiment)
            cur_date += timedelta(days=1)

        total_sentiment_per_day[res.id].append(negative)
        total_sentiment_per_day[res.id].append(positive)
        total_sentiment_per_day[res.id].append(neutral)
    # print(total_sentiment_per_day)
    context['total_sentiment_per_day'] = total_sentiment_per_day
    return JsonResponse(context)
