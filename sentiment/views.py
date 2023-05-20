from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from sentiment.crawl import crawl_tweet, MyStreamListener
from sentiment.scrape import scrape_tweet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from sentiment.models import Tweet, Bacapres
from .forms.bacapres_form import BacapresForm
from django.contrib import messages
from django.views.generic import CreateView
from . import preprocessing
from .preprocessing import TextPreprocessing
from sentigovt2.decorators import role_required
import pickle
import joblib
import json

vectorizer = pickle.load(open("TFIDFvec.pickle","rb"))
classifier = joblib.load("MultinomialNBModel.joblib")

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

def preprocessing(text):
    # data cleaning
    text = preprocessing.removeHashtagsMentionsUrl(text)
    text = preprocessing.removeHtmlTags(text)
    text = preprocessing.removeNonAscii(text)
    text = preprocessing.removePunctuation(text)
    text = preprocessing.removeWhitespaceLT(text)
    text = preprocessing.removeWhitespaceMultiple(text)
    text = preprocessing.removeMultipleChar(text)

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

def coba(request):
    return render(request, 'dashboard.html')

def bacapres_list(request):
    bacapres = Bacapres.objects.all()
    data = {}
    data['object_list'] = bacapres
    return render(request, 'bacapresManagement.html', data)

def create_bacapres(request):
    context = {}
    form = BacapresForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Bacapres was succesfully added!'))
            return render(request, 'bacapresManagement.html')
        else:
            messages.error(request, 'Error saving form')
            print(form.errors.as_data())
    context['form'] = form
    return render(request, 'createBacapres.html', context)


def edit_bacapres(request, id):
    context = {}
    bacapres = get_object_or_404(Bacapres,id=id)
    form = BacapresForm(request.POST or None, instance=bacapres)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('sentiment:create_bacapres'))
    context['form'] = form
    return render(request,'create_bacapres.html', context)

def delete_bacapres(request, id):
    context = {}
    bacapres = get_object_or_404(Bacapres, id=id)
    if request.method=='POST':
        return render(request,'create_bacapres.html', context)
