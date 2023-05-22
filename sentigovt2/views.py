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

    if 'selected_options' in request.session:
        del request.session['selected_options']
    tokoh_tweets = Tweet.objects.filter(bacapres=11).order_by('-created_at')

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
    bacapres = Bacapres.objects.all().order_by('id')
    if bacapres: context['active_item'] = bacapres.first()
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
        dates.append(date)
        cur_date += timedelta(days=1)

    return dates

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