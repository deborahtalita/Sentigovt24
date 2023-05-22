"""
URL configuration for sentigovt2 project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sentiment/', include('sentiment.urls', namespace='sentiment')),
    path('bacapres/', include('bacapres.urls', namespace='bacapres')),
    path('', include('accounts.urls', namespace='account')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manualSearch/', views.manualSearch, name='manualSearch'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('userManagement/', views.userManagement, name='userManagement'),
    path('getAllTotalSentiment/', views.getAllTotalSentiment, name='getAllTotalSentiment'),
    path('userManagement/editUser/', views.editUser, name='editUser'),
    # path('bacapresManagement/', views.bacapresManagement, name='bacapresManagement'),
    # path('bacapresManagement/createBacapres/', views.createBacapres, name='createBacapres'),
    # path('bacapresManagement/editBacapres/', views.editBacapres, name='editBacapres'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)