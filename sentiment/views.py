from django.shortcuts import render, get_object_or_404, redirect
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet, History
from bacapres.models import Bacapres
from accounts.models import User
from .preprocessing import TextPreprocessing
from sentigovt2.decorators import role_required
import pytz 
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .helpers.sentiment_helper import predict, orderLabel
from .helpers.date_helper import convertDate, getDates
from .helpers.session_helper import isGuestLimitAccess

# default time
timezone = pytz.timezone('Asia/Jakarta')
end_date = datetime.now(timezone).replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=6)

@csrf_exempt
def scrape(request):
    if request.method == 'POST':
        preprocessor = TextPreprocessing()
        data = scrape_tweet()

        data = preprocessor.removeIrrelevantTweet(data)
        result = []

        for i in range(0, len(data)):
            preprocessed_text = preprocessor.getFinalPreprocessingResult(data[i]['text'])
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

def manualSearch(request):
    context = {}
    if request.method == 'POST' and isGuestLimitAccess(request.COOKIES) == False:
        selected_options = request.POST.getlist('search_field')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        
        selected_options = [int(x) for x in selected_options[0].split(',')]

        # assign request to session
        request.session['selected_options'] = selected_options
        request.session['selected_start_date'] = start
        request.session['selected_end_date'] = end

        # get selected bacapres
        bacapres = getBacapres(request.session)
        context['bacapres'] = bacapres

        # get default selected bacapres
        active_item = bacapres.first()
        if active_item: context['active_item'] = active_item.id
        
        context['result'] = 'true'
        
        # set date to insert in history obj
        start_date = convertDate(start)
        end_date = convertDate(end)

        # get tweet to insert in history obj
        tweets = Tweet.objects.filter(created_at__range=(start_date,end_date)).filter(bacapres__in=selected_options)

        #  get auth user
        if request.user.is_authenticated:
            print(request.user.id)
            user = User.objects.get(id=request.user.id)
            history = History.objects.create(start_date=start_date,end_date=end_date,user=user)
        else:
            history = History.objects.create(start_date=start_date,end_date=end_date)

        #  save manual search to history

        history.bacapres.add(*bacapres)
        history.tweet.add(*tweets)
    # elif isGuestLimitAccess(request.COOKIES):
    #     context['result'] = False
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres_opt'] = bacapres 

    context['title'] = 'Manual Search'
    context['active_page'] = 'dashboard'
    return render(request, 'dashboard.html', context)

def getTrenTotalTweet(request):
    context = {}

    # get bacapres
    bacapres = getBacapres(request.session)

    # get tweets and dates
    tweet, start_date, end_date = getTweets(request.session)

    dates = getDates(start_date, end_date)
    context['dates'] = dates

    # get tren total tweet per bacapres per day
    bacapres_total_tweet_per_day = []
    for res in bacapres:
        series_data = {'name':res.name,'data':[]}
        cur_date = start_date
        tokoh_tweets = tweet.filter(bacapres=res.id)
        while cur_date <= end_date:
            day = cur_date + timedelta(days=1)
            total_tweet_per_day = tokoh_tweets.filter(created_at__range=(cur_date,day)).count()
            series_data['data'].append(total_tweet_per_day)
            cur_date += timedelta(days=1)
        bacapres_total_tweet_per_day.append(series_data)       
    context['bacapres_total_tweet_per_day'] = bacapres_total_tweet_per_day
    
    
    return JsonResponse(context)


def getTrenTotalSentiment(request):
    context = {}

    # get bacapres
    bacapres = getBacapres(request.session)

    # get tweets and dates
    tweet, start_date, end_date = getTweets(request.session)

    dates = getDates(start_date, end_date)
    context['dates'] = dates
    
    # get total tweet per classification per day
    total_sentiment_per_day = {}
    for res in bacapres:
        total_sentiment_per_day[res.id] = []
        negative = {'name':'Negative', 'data':[]}
        positive = {'name':'Positive', 'data':[]}
        neutral = {'name':'Neutral', 'data':[]}

        cur_date = start_date
        while cur_date <= end_date:
            day = cur_date + timedelta(days=1)
            tokoh_tweets = tweet.filter(bacapres=res.id).filter(created_at__range=(cur_date,day))

            neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
            pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
            neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
            
            negative['data'].append(neg_sentiment)
            positive['data'].append(pos_sentiment)
            neutral['data'].append(neu_sentiment)
            cur_date += timedelta(days=1)

        total_sentiment_per_day[res.id].append(negative)
        total_sentiment_per_day[res.id].append(positive)
        total_sentiment_per_day[res.id].append(neutral)
    
    context['total_sentiment_per_day'] = total_sentiment_per_day
    return JsonResponse(context)

def getTotalTweet(request):
    context= {}
    
    # get bacapres
    bacapres = getBacapres(request.session)

    # get tweets and dates
    tweet, _, _ = getTweets(request.session)
    
    # total tweet & tweet per sentiment
    bacapres_total_tweet = {}
    bacapres_total_sentiment = {}
    for res in bacapres:
        tokoh_tweets = tweet.filter(bacapres=res.id)
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
    return JsonResponse(context)

def getTweetList(request):
    context = {}
    global start_date, end_date

    # get bacapres
    bacapres = getBacapres(request.session)

    # get default selected bacapres
    bacapres = bacapres.first()
    active_item = bacapres.id
    
    # get tweets and dates
    tweet, _, _ = getTweets(request.session)

    # get tweets by selected bacapres
    bacapres_id = int(request.GET.get('bacapres', active_item))
    tokoh_tweets = tweet.filter(bacapres=bacapres_id).order_by('-created_at')

    # pagination
    paginator = Paginator(tokoh_tweets, 10)  # 10 items per page
    page_number = request.GET.get('page', 1)# Get the current page number from the request
    page_obj = paginator.get_page(page_number)
    
    data_items = []
    for item in page_obj:
        date = item.created_at
        data_item = {
            'no': item.id,
            'name': item.user_name,
            'tweet': item.text,
            'sentiment': item.sentiment,
            'date': date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
        }
        data_items.append(data_item)
    
    context = {
        'total_pages':paginator.num_pages,
        'results': data_items,
    }
    
    return JsonResponse(context)

def getTweets(session):
    global start_date, end_date

    # get tweets
    if ('selected_start_date' in session) and ('selected_end_date' in session): # for manual search
        start_date = convertDate(session['selected_start_date'])
        end_date = convertDate(session['selected_end_date'])
        tweet = Tweet.objects.filter(created_at__range=(start_date,end_date))
        
    elif 'history_id' in session: # for history detail
        history_id = session['history_id']
        history = History.objects.get(id=history_id)
        tweet = history.tweet.all() # get tweet based on history

        start_date = history.start_date
        end_date = history.end_date
    tweets = Tweet.objects.filter(created_at__range=(start_date,end_date))
    return tweets, start_date, end_date

def getBacapres(session):
    # get bacapres
    if 'selected_options' in session:
        selected_options = session['selected_options']
        bacapres = Bacapres.objects.filter(id__in=selected_options).order_by('id')
    else:
        bacapres = Bacapres.objects.all().order_by('id')
    
    return bacapres

####################### HISTORY #######################
@role_required(allowed_roles=['MEMBER', 'ADMIN', 'SUPERADMIN'])
def getHistoryList(request):
    context = {}

    # get history
    user = User.objects.get(id=request.user.id)
    history = History.objects.filter(user=user).prefetch_related('bacapres').all().order_by('id')

    #  pagination
    paginator = Paginator(history, 10)
    page_number = request.GET.get('page', 1)# Get the current page number from the request
    page_obj = paginator.get_page(page_number)

    data_items = []
    for item in page_obj:
        bacapres_items = []
        startDate = item.start_date
        endDate = item.end_date
        for b_item in item.bacapres.all():
            bacapres_items.append(b_item.name)
        data_item = {
            'no': item.id,
            'bacapres': bacapres_items,
            'start_date': startDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': endDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
        }
        data_items.append(data_item)
    print(data_items)
    context = {
        'total_pages':paginator.num_pages,
        'results': data_items,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context, safe=False)
    else:
        context['active_page'] = 'history'
        return render(request, 'history/history.html', context)

@role_required(allowed_roles=['MEMBER', 'ADMIN', 'SUPERADMIN'])
def getDetailHistory(request, id):
    context = {}

    # belum ada pengecekan user id sesuai gak
    history = get_object_or_404(History, id=id)

    # assign history id and selected options to session
    bacapres = history.bacapres.all()
    selected_options = [obj.id for obj in bacapres]

    request.session['selected_options'] = selected_options
    request.session['history_id'] = history.id

    # get selected bacapres
    bacapres = getBacapres(request.session)
    context['bacapres'] = bacapres

    # get default selected bacapres
    active_item = bacapres.first()
    if active_item: context['active_item'] = active_item.id

    context['title'] = 'History'
    context['active_page'] = 'history'

    return render(request, 'dashboard.html', context)

@role_required(allowed_roles=['MEMBER', 'ADMIN', 'SUPERADMIN'])
def deleteHistory(request, id):
    context = {}
    try:
        history = get_object_or_404(History, id=id)
        history.delete()
        # return redirect(reverse_lazy('sentiment:getHistoryList'))
        return JsonResponse({'message': 'Data deleted successfully'})
    except History.DoesNotExist:
        print("Object not found")
        # return redirect(reverse_lazy('sentiment:getHistoryList'))
        return JsonResponse({'message': 'Invalid request method'})