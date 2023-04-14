from django.urls import path

from . import views

urlpatterns = [
    path('crawl', views.crawl, name="index"),
    path('scrape', views.scrape, name="index"),
]