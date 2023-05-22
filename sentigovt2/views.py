from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from sentiment.models import Tweet, Bacapres
import uuid
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
import pytz 
from django.http import JsonResponse

# get times
dt_utc = datetime.utcnow()
timezone = pytz.timezone('Asia/Jakarta')
today = dt_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
seven_days_ago = today - timedelta(days=7)

# Create your views here.
def setcookie(request):
    unique_id = str(uuid.uuid4())
    response = HttpResponse("Cookie baru telah diatur.")
    response.set_cookie('session_id', unique_id)
    print(response)
    return response

def home(request):
    # setcookie(request)
    rendered_html = render(request, 'home.html')
    session_id = request.COOKIES.get('session_id')
    if session_id:
        response = HttpResponse(rendered_html)
    else:
        response = HttpResponse(rendered_html)
        
        unique_id = str(uuid.uuid4())
        response.set_cookie('session_id', unique_id, max_age=3600)
    return response

@login_required
def dashboard(request):
    context = {}
    dt_utc = datetime.utcnow()
    timezone = pytz.timezone('Asia/Jakarta')
    today = dt_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
    print(today.tzinfo)
    date = today.day
    month = today.month
    year = today.year
    counter = Tweet.objects

    seven_days_ago = today - timedelta(days=7)
    tweet = Tweet.objects.filter(created_at__gte=seven_days_ago)

    # total tweet per day per classification
    counter = tweet.extra({
        'created_at': "date(created_at)"
    }).values('created_at').distinct().annotate(Count('created_at'))

    dates = []
    dates_counter = []

    for i in counter:
        dates.append(str(i['created_at']))
        # print(i['created_at'])
        dates_counter.append(i['created_at__count'])
    
    context['dates'] = dates
    context['dates'] = ['2023-05-15', '2023-05-16', '2023-05-17', '2023-05-18', '2023-05-19', '2023-05-20', '2023-05-21']
    context['pos_sentiment'] = [45, 52, 38, 45, 19, 23, 2]
    context['neg_sentiment'] = [10, 25, 12, 32, 41, 20, 36]
    context['neu_sentiment'] = [30, 20, 15, 40, 45, 50, 5]
    # print(dates)


    tokoh_tweets = Tweet.objects.filter(bacapres=11)

    # total tweet
    total = tokoh_tweets.count()
    context['total_tweet'] = total

    neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
    pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
    neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
    
    # total tweet per classification
    context['sentiment'] = {'negative':neg_sentiment,
                            'positive':pos_sentiment,
                            'neutral':neu_sentiment}

    # get bacapres
    bacapres = Bacapres.objects.all()
    context['bacapres'] = bacapres

    #tweet list with pagination
    paginator = Paginator(tokoh_tweets, 10)  # 10 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    context['title'] = 'Dashboard'
    context['active_page'] = 'dashboard'
    return render(request, 'dashboard.html', context)

def getDates():
    dates = []
    i = 0

    cur_date = seven_days_ago
    while cur_date < today:
        date = cur_date.strftime('%Y-%m-%d') 
        print(cur_date.strftime('%Y-%m-%d'))
        dates.append(date)
        cur_date += timedelta(days=1)

    return dates


def getAllTotalTweet(request):
    context = {}
    dt_utc = datetime.utcnow()
    timezone = pytz.timezone('Asia/Jakarta')
    today = dt_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
    print(today.tzinfo)
    date = today.day
    month = today.month
    year = today.year
    counter = Tweet.objects

    # total tweet per day per classification
    counter = tweet.extra({
        'created_at': "date(created_at)"
    }).values('created_at').distinct().annotate(Count('created_at'))

    dates = []
    dates_counter = []

    for i in counter:
        dates.append(str(i['created_at']))
        # print(i['created_at'])
        dates_counter.append(i['created_at__count'])
    
    context['dates'] = dates

    seven_days_ago = today - timedelta(days=7)
    tweet = Tweet.objects.filter(created_at__gte=seven_days_ago)

    # get bacapres
    bacapres = Bacapres.objects.all().order_by('id')
    # print(bacapres)
    context['bacapres'] = bacapres

    # get tren total tweet per bacapres per day
    bacapres_total_tweet_per_day = {}
    cur_date = seven_days_ago
    for res in bacapres:
        bacapres_total_tweet_per_day[res.id] = []
        while cur_date <= today:
            # print(cur_date.strftime('%Y-%m-%d'))
            total_tweet_per_day = tweet.filter(bacapres=res.id).filter(created_at=cur_date).count()
            # print(total_tweet_per_day)
            bacapres_total_tweet_per_day[res.id].append(total_tweet_per_day)
            # print(bacapres_total_tweet_per_day[res.id])
            cur_date += timedelta(days=1)
    context['bacapres_total_tweet_per_day'] = bacapres_total_tweet_per_day
    return JsonResponse(context)

def getAllTotalSentiment(request):
    context = {}

    dates = getDates()
    context['dates'] = dates
    print(dates)

    # get bacapres
    bacapres = Bacapres.objects.all().order_by('id')
    # context['bacapres'] = bacapres

    # get tweets
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
            print(date)

            neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
            print("neg_sentiment",neg_sentiment)
            pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
            print("pos_sentiment",pos_sentiment)
            neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
            print("neu_sentiment",neu_sentiment)
            
            negative['data'].append(neg_sentiment)
            positive['data'].append(pos_sentiment)
            neutral['data'].append(neu_sentiment)
            cur_date += timedelta(days=1)

        total_sentiment_per_day[res.id].append(negative)
        total_sentiment_per_day[res.id].append(positive)
        total_sentiment_per_day[res.id].append(neutral)
    print(total_sentiment_per_day)
    context['total_sentiment_per_day'] = total_sentiment_per_day
    return JsonResponse(context)

def manualSearch(request):
    context = {}

    # bacapres
    bacapres = Bacapres.objects.all()
    context['bacapres'] = bacapres

    context['active_page'] = 'manual search'
    context['title'] = 'Manual Search'
    return render(request, 'dashboard.html', context)

def profile(request):
    return render(request, 'profile.html')

def history(request):
    context = {'active_page': 'history'}
    return render(request, 'history.html', context)

def userManagement(request):
    context = {'active_page': 'user management'}
    return render(request, 'userManagement.html', context)

def editUser(request):
    context = {'active_page': 'user management'}
    return render(request, 'editUser.html', context)

def createBacapres(request):
    context = {'active_page': 'bacapres management'}
    return render(request, 'createBacapres.html', context)

def editBacapres(request):
    context = {'active_page': 'bacapres management'}
    return render(request, 'editBacapres.html', context)