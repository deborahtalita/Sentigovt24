"""
URL configuration for sentigov24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manualSearch/', views.manualSearch, name='manualSearch'),
    path('get-data/', views.get_data, name='get_data'),
    path('get-data-table-dashboard/', views.get_data_table_dashboard, name='get_data_table_dashboard'),
    path('get-data-table-history/', views.get_data_table_history, name='get_data_table_history'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('history/detailHistory/', views.detailHistory, name='detailHistory'),
    path('userManagement/', views.userManagement, name='userManagement'),
    path('userManagement/editUser/', views.editUser, name='editUser'),
    path('bacapresManagement/', views.bacapresManagement, name='bacapresManagement'),
    path('bacapresManagement/createBacapres/', views.createBacapres, name='createBacapres'),
    path('bacapresManagement/editBacapres/', views.editBacapres, name='editBacapres'),
]
