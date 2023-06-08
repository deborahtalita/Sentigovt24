from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


app_name = 'account'

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutRequest, name="logout"),
    path('profile', views.UserProfileView.as_view(), name="profile"),
    path('account', views.AccountListView.as_view(), name="userManagement"),
    path('account/delete/<int:id>', views.AccountListView.as_view(), name="deleteUser"),
    path('account/edit/<int:id>', views.AccountDetailView.as_view(), name="editUser")
    # path('account/edit/<int:id>', views.editUser, name="editUser")
]