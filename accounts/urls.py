from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register', views.register, name="register"),
    path('register-success', views.regsuccess, name="regsuccess"),
    path('login/', views.webLoginView.as_view(), name='login'),
    path('logout/', views.logout_request, name="logout"),
    path('login-success', views.loginsuccess, name="logsuccess"),
]