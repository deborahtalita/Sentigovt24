from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sentiment'

urlpatterns = [
    path('scrape', views.scrape, name="index"),
    path('getscrapedtweet', views.getScrapedTweet, name="getScrapedTweet"),
    path('search', views.manualSearch, name="manualSearch"),
    path('getTrenTotalSentiment/', views.getTrenTotalSentiment, name='getTrenTotalSentiment'),
    path('getTrenTotalTweet/', views.getTrenTotalTweet, name='getTrenTotalTweet'),
    path('getTotalTweet/', views.getTotalTweet, name='getTotalTweet'),
    path('getTweetList', views.getTweetList, name='getTweetList'),
    path('history', views.HistoryView.as_view(), name="getHistoryList"),
    path('history/detail/<int:id>', views.HistoryDetailView.as_view(), name="getDetailHistory"),
    path('history/delete/<int:id>', views.deleteHistory, name="deleteHistory"),
    path('getBacapresRanking', views.getRankingBacapres, name="getRankingBacapres"),
    path('generateCSV', views.generateCSV, name="generateCSV"),
    # path('view', views.coba, name="index"),
]
        
        