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
seven_days_ago = today - timedelta(days=6)

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

def dashboard(request):
    context = {}

    if 'selected_options' in request.session:
        del request.session['selected_options']
    
    if 'selected_start_date' in request.session:
        del request.session['selected_start_date']
    
    if 'selected_end_date' in request.session:
        del request.session['selected_end_date']

    # get bacapres
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres'] = bacapres

    #  get tweets
    tweets = Tweet.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')

    # total tweet & tweet per sentiment
    bacapres_total_tweet = {}
    bacapres_total_sentiment = {}
    for res in bacapres:
        tokoh_tweets = tweets.filter(bacapres=res.id)
        total = tokoh_tweets.count()
        bacapres_total_tweet[res.id] = total

        neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
        pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
        neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
        bacapres_total_sentiment[res.id] = {'negative':neg_sentiment,
                                            'positive':pos_sentiment,
                                            'neutral':neu_sentiment}
    context['bacapres_total_tweet'] = bacapres_total_tweet
    context['bacapres_total_sentiment'] = bacapres_total_sentiment
    
    active_item = bacapres.first()
    if active_item: context['active_item'] = active_item.id
    
    print(active_item.id)

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
    while cur_date <= today:
        date = cur_date.strftime('%Y-%m-%d') 
        dates.append(date)
        cur_date += timedelta(days=1)

    return dates