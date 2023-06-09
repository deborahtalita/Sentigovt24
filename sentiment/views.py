from django.shortcuts import render, get_object_or_404, redirect
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from sentiment.models import Tweet, History, ScrapedTweet
from bacapres.models import Bacapres
from accounts.models import User
from .preprocessing import TextPreprocessing
from sentigovt2.decorators import role_required
from django.urls import reverse_lazy
import pytz 
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .helpers.sentiment_helper import predict, orderLabel
from .helpers.date_helper import convertStartDate, convertEndDate, getDates, today, last_seven_days
from .helpers.session_helper import isGuestLimitAccess
from sentigovt2.mixin import RoleRequiredMixin
from django.views import View
import csv

# default time
timezone = pytz.timezone('Asia/Jakarta')
end_date = datetime.now(timezone).replace(hour=23, minute=59, second=59, microsecond=59)
start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6)

@csrf_exempt
def scrape(request):
    if request.method == 'POST':
        preprocessor = TextPreprocessing()
        data = scrape_tweet()

        data = preprocessor.removeIrrelevantTweet(data)
        result = []
        i = 1

        for i in range(0, len(data)):
            preprocessed_text = preprocessor.getFinalPreprocessingResult(data[i]['text'])
            sentiment = predict(preprocessed_text)

            bacapres = Bacapres.objects.get(id=data[i]['bacapres'])

            obj_tweet = Tweet(
                tweet_id = data[i]['tweet_id'],
                text = data[i]['text'],
                text_preprocessed = preprocessed_text,
                created_at = data[i]['created_at'],
                user_name = data[i]['user_name'],
                sentiment = orderLabel(sentiment),
                bacapres = bacapres
            )
            print(i)
            i=i+1
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
    if request.method == 'POST':
        if 'session_guest' in request.COOKIES and isGuestLimitAccess(request):
            context['result'] = False
        else:
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
            start_date = convertStartDate(start)
            end_date = convertEndDate(end)

            # get tweet to insert in history obj
            tweets = Tweet.objects.filter(created_at__range=(start_date,end_date)).filter(bacapres__in=selected_options)

            #  get auth user
            if request.user.is_authenticated:
                user = User.objects.get(id=request.user.id)
                history = History.objects.create(start_date=start_date,end_date=end_date,user=user)

                #  save manual search to history
                history.bacapres.add(*bacapres)
                history.tweet.add(*tweets)
    
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres_opt'] = bacapres 

    context['title'] = 'Manual Search'
    context['active_page'] = 'manual search'
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

    # get default selected bacapres
    bacapres = bacapres.first()
    active_item = bacapres.id

    # get selected bacapres
    bacapres_id = int(request.GET.get('bacapres', active_item))
    bacapres = Bacapres.objects.filter(id=bacapres_id)

    # get tweets and dates
    tweet, start_date, end_date = getTweets(request.session)

    dates = getDates(start_date, end_date)
    context['dates'] = dates
    
    # get total tweet per classification per day
    total_sentiment_per_day = []
    negative = {'name':'Negative', 'data':[]}
    positive = {'name':'Positive', 'data':[]}
    neutral = {'name':'Neutral', 'data':[]}

    cur_date = start_date
    while cur_date <= end_date:
        day = cur_date + timedelta(days=1)
        tokoh_tweets = tweet.filter(bacapres=bacapres_id).filter(created_at__range=(cur_date,day))

        neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
        pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
        neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
        
        negative['data'].append(neg_sentiment)
        positive['data'].append(pos_sentiment)
        neutral['data'].append(neu_sentiment)
        cur_date += timedelta(days=1)

    total_sentiment_per_day.append(negative)
    total_sentiment_per_day.append(positive)
    total_sentiment_per_day.append(neutral)
    
    context['total_sentiment_per_day'] = total_sentiment_per_day
    print(total_sentiment_per_day)
    return JsonResponse(context)

def getTotalTweet(request):
    context= {}
    
    # get bacapres
    bacapres = getBacapres(request.session)

    # get default selected bacapres
    bacapres = bacapres.first()
    active_item = bacapres.id

    # get selected bacapres
    bacapres_id = int(request.GET.get('bacapres', active_item))
    bacapres = Bacapres.objects.filter(id=bacapres_id)

    # get tweets and dates
    tweet, _, _ = getTweets(request.session)
    
    # total tweet & tweet per sentiment
    tokoh_tweets = tweet.filter(bacapres=bacapres_id)
    total = tokoh_tweets.count()
    bacapres_total_tweet = total

    neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
    pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
    neu_sentiment = tokoh_tweets.filter(sentiment='neutral').count()
    bacapres_total_sentiment= {'negative':neg_sentiment,
                                'positive':pos_sentiment,
                                'neutral':neu_sentiment}
    context['bacapres_total_tweet'] = bacapres_total_tweet
    context['bacapres_total_sentiment'] = bacapres_total_sentiment
    print(bacapres_total_tweet)
    print(bacapres_total_sentiment)
    return JsonResponse(context)

def getRankingBacapres(request):
    context = {}

    # get bacapres
    bacapres = getBacapres(request.session)
    tweet, _, _ = getTweets(request.session)
    # option = request.GET.get('option', 'positive')
    
    
    bacapres_rank = []
    for res in bacapres:
        tokoh_tweets = tweet.filter(bacapres=res.id)
        pos_sentiment = tokoh_tweets.filter(sentiment='positive').count()
        neg_sentiment = tokoh_tweets.filter(sentiment='negative').count()
        bacapres = {
            'id':res.id,
            'name': res.name,
            'img_bacapres': res.avatar.url,
            'positive': pos_sentiment,
            'negative': neg_sentiment,
        }
        bacapres_rank.append(bacapres)
        # sorted_data = sorted(bacapres_rank, key=lambda x: x['value'], reverse=True)
    context['results'] = bacapres_rank
    
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
        date = item['created_at']
        data_item = {
            'no': item['id'],
            'name': item['user_name'],
            'tweet': item['text'],
            'sentiment': item['sentiment'],
            'date': date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
        }
        data_items.append(data_item)
    
    context = {
        'total_pages':paginator.num_pages,
        'results': data_items,
    }
    
    return JsonResponse(context)

@role_required(allowed_roles=['MEMBER', 'ADMIN', 'SUPERADMIN'])
def generateCSV(request):
    # get tweets and dates
    tweet, start_date, end_date = getTweets(request.session)

    # get tweets by selected bacapres
    bacapres_id = request.GET.get('bacapres')
    data = tweet.filter(bacapres=bacapres_id).order_by('-created_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['No','User name', 'Tweet', 'Sentiment', 'Date'])  # Write header row

    for index, obj in enumerate(data, start=1):
        date = obj['created_at'].astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([index, obj['user_name'], obj['text'], obj['sentiment'], date])  # Write each row with the desired fields

    return response


def getTweets(session):
    # get tweets
    if ('selected_start_date' in session) and ('selected_end_date' in session): # for manual search
        start_date = convertStartDate(session['selected_start_date'])
        end_date = convertEndDate(session['selected_end_date'])
        
    elif 'history_id' in session: # for history detail
        history_id = session['history_id']
        history = History.objects.get(id=history_id)

        start_date = history.start_date
        end_date = history.end_date
    else:
        start_date = last_seven_days # from date_helper to get current dates
        end_date = today
    tweets = Tweet.objects.filter(created_at__range=(start_date,end_date)).values('id','user_name','text','created_at','sentiment','bacapres')
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

class HistoryView(RoleRequiredMixin, View):
    required_roles = ['MEMBER', 'ADMIN', 'SUPERADMIN']
    context = {}
    context['active_page'] = 'history'
    template_name = 'history/history.html'

    def get(self, request):
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
            for b_item in item.bacapres.all().order_by('name'):
                bacapres_items.append(b_item.name)
            data_item = {
                'no': item.id,
                'bacapres': bacapres_items,
                'start_date': startDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': endDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
            }
            data_items.append(data_item)

        self.context['total_pages'] = paginator.num_pages
        self.context['results'] = data_items

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(self.context, safe=False)
        else:
            return render(request, self.template_name, self.context)
        
class HistoryDetailView(RoleRequiredMixin, View):
    required_roles = ['MEMBER', 'ADMIN', 'SUPERADMIN']
    context = {}
    context['active_page'] = 'history'
    context['title'] = 'History'
    template_name = 'dashboard.html'

    def get(self, request, id):
        # belum ada pengecekan user id sesuai gak
        history = get_object_or_404(History, id=id)

        # get dates
        self.context['startDate'] = history.start_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
        self.context['endDate'] = history.end_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")

        # assign history id and selected options to session
        bacapres = history.bacapres.all()
        selected_options = [obj.id for obj in bacapres]

        request.session['selected_options'] = selected_options
        request.session['history_id'] = history.id

        # get selected bacapres
        bacapres = getBacapres(request.session)
        self.context['bacapres'] = bacapres

        # get default selected bacapres
        active_item = bacapres.first()
        if active_item: self.context['active_item'] = active_item.id

        return render(request, self.template_name, self.context)

class HistoryDeleteAllView(RoleRequiredMixin, View):
    required_roles = ['MEMBER', 'ADMIN', 'SUPERADMIN']
    context = {}
    context['active_page'] = 'history'

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        History.objects.filter(user=user).delete()
        return redirect(reverse_lazy('sentiment:getHistoryList'))

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
        for b_item in item.bacapres.all().order_by('name'):
            bacapres_items.append(b_item.name)
        data_item = {
            'no': item.id,
            'bacapres': bacapres_items,
            'start_date': startDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': endDate.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
        }
        data_items.append(data_item)
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
    context = {
        'startDate' : history.start_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
        'endDate' : history.end_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"),
    }

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
        
        return JsonResponse({'message': 'Data deleted successfully'})
    except History.DoesNotExist:
        print("Object not found")
        return JsonResponse({'message': 'Invalid request method'})
