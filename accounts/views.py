from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import logout
from .forms import SignUpForm, UpdateProfileForm
from .models import User
from sentigovt2.decorators import role_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

def register(request):
    context = {}
    context['registered'] = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect(reverse_lazy('dashboard'))
    else:
        form = SignUpForm()
        # print(form.errors.as_data())
    context['form'] = form
    # print(form)
    return render(request, 'accounts/register.html',context)

def logoutRequest(request):
    logout(request)
    print("berhasil logout")
    return redirect(reverse_lazy('home'))

def editProfile(request):
    context = {}
    auth_user = request.user

    user = get_object_or_404(User,id=auth_user.id)
    form = UpdateProfileForm(request.POST,request.FILES, instance=user)
    print(form)
    if request.method == "POST":
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.avatar = form.cleaned_data['avatar']
            user.username = form.cleaned_data['email']
            if not user.avatar:
                user.avatar = User.objects.get(id=auth_user.id).avatar
            user.save()
            return redirect(reverse_lazy('account:profile'))
        else:
            print(form.errors.as_data())
    context['form'] = form
    context['user'] = user
    return render(request, 'accounts/profile.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def userAccountList(request):
    # get user
    user = User.objects.all().filter(is_active=True).order_by('id')

    # pagination
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    data_items = []
    for item in page_obj:
        data_item = {
            'id': item.id,
            'name': item.first_name,
            'role': item.role,
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
        context['active_page'] = 'bacapres management'
        return render(request, 'accounts/userManagement.html', context)

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
    user = get_object_or_404(User,id=id)
    if request.method == "POST":
        role = request.POST.get('selected_role')
        user.role = role
        user.save()
    context['user'] = user
    return render(request,'accounts/editUser.html', context)

class LoginView(View):
    context = {}
    template_name = 'accounts/login.html'

    def get(self, request):
        self.context['verifikasi'] = False
        return render(request, self.template_name, self.context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            self.context['verified'] = False
            return render(request, self.template_name, self.context)

