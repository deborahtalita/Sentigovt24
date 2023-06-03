from django.shortcuts import render
from django.http import HttpResponse
from sentiment.models import Bacapres
import uuid
from accounts.models import Session
from sentiment.views import getBacapres, getTweets


def home(request):
    
    return render(request, 'home.html')

def dashboard(request):
    context = {}

    if 'selected_options' in request.session:
        del request.session['selected_options']
    
    if 'selected_start_date' in request.session:
        del request.session['selected_start_date']
    
    if 'selected_end_date' in request.session:
        del request.session['selected_end_date']
    
    if 'history_id' in request.session:
        del request.session['history_id']

    # get bacapres
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres'] = bacapres

    active_item = bacapres.first()
    if active_item: context['active_item'] = active_item.id

    context['title'] = 'Dashboard'
    context['active_page'] = 'dashboard'


    # bacapres = getBacapres(request.session)
    # tweet, _, _ = getTweets(request.session)
    # option = request.GET.get('option', 'positive')
    
    # bacapres_rank = []
    # for res in bacapres:
    #     tokoh_tweets = tweet.filter(bacapres=res.id)
    #     selected_sentiment = tokoh_tweets.filter(sentiment=option).count()
    #     bacapres = {'id':res.id, 'name':res.name, 'value':selected_sentiment, 'avatar':res.avatar.url}
    #     bacapres_rank.append(bacapres)
    # context['bacapres_rank'] = bacapres_rank
    # sorted_data = sorted(bacapres_rank, key=lambda x: x['value'], reverse=True)
    # context['sorted_data'] = sorted_data
    # print(sorted_data)
    rendered_html = render(request, 'dashboard.html', context)

    # set session for guest
    session_guest = request.COOKIES.get('session_guest')
    if session_guest:
        response = HttpResponse(rendered_html)
    else:
        response = HttpResponse(rendered_html)
        
        unique_id = str(uuid.uuid4())
        session_age = 3600 * 24 * 90 # 3 months
        response.set_cookie('session_guest', unique_id, max_age=session_age)
        session = Session.objects.create(id=unique_id)
        print(unique_id)
        # session.save()

    return response