from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sentiment'

urlpatterns = [
    path('crawl', views.crawl, name="index"),
    path('scrape', views.scrape, name="index"),
    path('test', views.preprocess, name="index"),
    path('search', views.search, name="search"),
    path('getAllTotalSentiment/<int:id>', views.getAllTotalSentiment, name='getAllTotalSentiment'),
    path('getAllTotalTweet/', views.getAllTotalTweet, name='getAllTotalTweet'),
    path('history', views.getHistoryList, name="getHistoryList")
    # path('view', views.coba, name="index"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)