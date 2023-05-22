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
               'verifikasi_confirmPassword':'true'
               }
    return render(request, 'register.html', context)

def dashboard(request):
    context = {}
    dummy_list = ['Ganjar Pranowo', 'Anies Baswedan', 'Puan Maharani', 'Ridwan Kamil']
    if dummy_list: context['active_item'] = dummy_list[0]
    context['dates'] = ['2023-05-15', '2023-05-16', '2023-05-17', '2023-05-18', '2023-05-19', '2023-05-20', '2023-05-21']
    context['active_page'] = 'dashboard'
    context['title'] = 'Dashboard'
    context['dummy_list'] = dummy_list
    return render(request, 'dashboard.html', context)

def get_data(request):
    context = [
        {
            'name': 'Positive',
            'data': [45, 52, 38, 45, 19, 23, 2],
        },
        {
            'name': 'Neutral',
            'data':  [10, 25, 12, 32, 41, 20, 36],
        },
        {
            'name': 'Negative',
            'data':  [30, 20, 15, 40, 45, 50, 5],
        }
    ]
    return JsonResponse({'series': context})

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