from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


app_name = 'account'

urlpatterns = [
    path('register', views.register, name="register"),
    path('login/', views.webLoginView.as_view(), name='login'),
    path('logout/', views.logoutRequest, name="logout"),
    path('profile', views.getProfile, name="profile"),
    path('account', views.userAccountList, name="userManagement"),
    path('account/delete/<int:id>', views.deleteUser, name="deleteUser"),
    path('editUser/<int:id>', views.editUser, name="editUser")
]