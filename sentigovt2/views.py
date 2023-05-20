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

    seven_days_ago = today - timedelta(days=6)
    tweet = Tweet.objects.filter(created_at__gte=seven_days_ago)

    # total tweet per day per classification
    counter = tweet.extra({
        'created_at': "date(created_at)"
    }).values('created_at').distinct().annotate(Count('created_at'))

    dates = []
    dates_counter = []

    for i in counter:
        dates.append(i['created_at'])
        dates_counter.append(i['created_at__count'])
    
    context['dates'] = dates


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
    context['pos_sentiment'] = pos_sentiment
    context['neu_sentiment'] = neu_sentiment

    # ranking bacapres
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

def manualSearch(request):
    context = {'active_page': 'manual search'}
    return render(request, 'manualSearch.html', context)

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