from django.shortcuts import render

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
    context = {'active_page': 'dashboard',
               'title': 'Dashboard'
               }
    return render(request, 'dashboard.html', context)

def manualSearch(request):
    context = {'active_page': 'manual search',
               'title': 'Manual Search'
               }
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