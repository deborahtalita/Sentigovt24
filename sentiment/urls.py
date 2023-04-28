from django.urls import path

from . import views

urlpatterns = [
    path('crawl', views.crawl, name="index"),
    path('scrape', views.scrape, name="index"),
    path('bacapres', views.create_bacapres, name="bacapres"),
    path('stream', views.stream, name="stream"),
]