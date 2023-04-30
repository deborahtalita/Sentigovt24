from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, LoginForm

# Create your views here.

def register(request):
    context = {}
    form = SignUpForm(request.POST,request.FILES)
    context['registered'] = False
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return render(request, 'success-register.html')
        else:
            print(form.errors.as_data())
    context['form'] = form
    return render(request, 'register.html',context)

def regsuccess(request):
    return render(request, 'success-register.html')

@login_required
def loginsuccess(request):
    return render(request, 'success-login.html')

class webLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    # success_url = reverse_lazy('logsuccess')
    # redirect_authenticated_user = True

    # def form_invalid(self, form):
    #     messages.error(self.request,'Invalid email or password')
    #     return self.render_to_response(self.get_context_data(form=form))