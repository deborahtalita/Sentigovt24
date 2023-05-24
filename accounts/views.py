from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import SignUpForm, LoginForm
from .models import User
from sentigovt2.decorators import role_required

# Create your views here.

def register(request):
    context = {}
    form = SignUpForm(request.POST)
    context['registered'] = False
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('dashboard'))
        else:
            print(form.errors.as_data())
    context['form'] = form
    print(form)
    return render(request, 'register.html',context)

def logoutRequest(request):
    logout(request)
    print("berhasil logout")
    return render(request,'home.html')

def getProfile(request):
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'profile.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def userAccountList(request):
    user = User.objects.all().filter(is_active=True).order_by('id')
    data = {}
    data['obj_list'] = user
    return render(request, 'userManagement.html', data)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def deleteUser(request, id):
    context = {}
    try:
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        user.save()
        print(user.save())
        return redirect(reverse_lazy('account:userManagement'))
    except User.DoesNotExist:
        print("Object not found")
        return redirect(reverse_lazy('account:userManagement'))

def editUser(request, id):
    context = {}
    # bacapres = get_object_or_404(User,id=id)
    # form = UserCreationForm(request.POST or None, instance=bacapres)
    # if request.method == "POST":
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse_lazy('bacapres:bacapres_list'))
    # context['form'] = form
    # context['object'] = bacapres
    return render(request,'editBacapres.html', context)

class webLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
