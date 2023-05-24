from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def login(request):
    context = {'verifikasi_email': 'true',
               'verifikasi_password': 'true'
               }
    return render(request, 'login.html', context)


def register(request):
    context = {'verifikasi_email': 'true',
               'verifikasi_password': 'true',
               'verifikasi_confirmPassword': 'true'
               }
    return render(request, 'register.html', context)


def dashboard(request):
    context = {}
    dummy_list = ['Ganjar Pranowo', 'Anies Baswedan', 'Puan Maharani', 'Ridwan Kamil']
    if dummy_list:
        context['active_item'] = dummy_list[0]
    context['active_page'] = 'dashboard'
    context['title'] = 'Dashboard'
    bacapres = [
        {'id': 1, 'name': 'Ganjar Pranowo'},
        {'id': 2, 'name': 'Anies Baswedan'},
        {'id': 3, 'name': 'Puan Maharani'},
        {'id': 4, 'name': 'Ridwan Kamil'}
    ]
    context['bacapres'] = bacapres
    context['dummy_list'] = dummy_list
    return render(request, 'dashboard.html', context)


def get_data(request):
    context = {}
    context['series'] = {1: [{'name': 'Negative', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Positive', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Neutral', 'data': [1, 1, 1, 1, 1, 1, 1]}], 
                         2: [{'name': 'Negative', 'data': [1, 1, 1, 100, 1, 100, 1]}, {'name': 'Positive', 'data': [1, 1, 1, 300, 1, 1, 1]}, {'name': 'Neutral', 'data': [1, 300, 350, 1, 1, 1, 1]}], 
                         3: [{'name': 'Negative', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Positive', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Neutral', 'data': [1, 1, 1, 1, 1, 1, 1]}], 
                         4: [{'name': 'Negative', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Positive', 'data': [1, 1, 1, 1, 1, 1, 1]}, {'name': 'Neutral', 'data': [1, 1, 1, 1, 1, 1, 1]}], }
    context['dates'] = ['2023-05-15', '2023-05-16', '2023-05-17',
                        '2023-05-18', '2023-05-19', '2023-05-20', '2023-05-21']
    context['total_tweet'] = {1: 20, 2: 25, 3: 50, 4: 40, 5: 125, 6: 600, 7: 39, 8: 43, 9: 21, 10: 1235}
    context['total_sentiment'] = {1: {'negative': 5, 'positive': 5, 'neutral': 10}, 
                                  2: {'negative': 1, 'positive': 6, 'neutral': 9}, 
                                  3: {'negative': 2, 'positive': 7, 'neutral': 8}, 
                                  4: {'negative': 3, 'positive': 8, 'neutral': 7}}
    return JsonResponse(context)


def manualSearch(request):
    context = {}
    context['active_page'] = 'manual search'
    context['title'] = 'Manual Search'
    context['result'] = 'false'
    return render(request, 'dashboard.html', context)


def profile(request):
    return render(request, 'profile.html')


def history(request):
    context = {'active_page': 'history'}
    return render(request, 'history.html', context)


def detailHistory(request):
    context = {'active_page': 'history',
               'title': 'History'}
    return render(request, 'dashboard.html', context)


def userManagement(request):
    context = {'active_page': 'user management'}
    return render(request, 'userManagement.html', context)


def editUser(request):
    context = {'active_page': 'user management'}
    return render(request, 'editUser.html', context)


def bacapresManagement(request):
    context = {'active_page': 'bacapres management'}
    return render(request, 'bacapresManagement.html', context)


def createBacapres(request):
    context = {'active_page': 'bacapres management'}
    return render(request, 'createBacapres.html', context)


def editBacapres(request):
    context = {'active_page': 'bacapres management'}
    return render(request, 'editBacapres.html', context)
