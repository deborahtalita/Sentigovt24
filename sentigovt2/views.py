from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from sentiment.models import Tweet, Bacapres
import uuid
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
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

    i = 1
    for t in tweet:
        i=i+1
    print(i)
    print(counter)

    # ranking bacapres
    bacapres = Bacapres.objects.all()
    context['bacapres'] = bacapres

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