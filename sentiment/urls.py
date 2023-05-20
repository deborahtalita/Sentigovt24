from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sentiment'

urlpatterns = [
    path('crawl', views.crawl, name="index"),
    path('scrape', views.scrape, name="index"),
    path('test', views.preprocess, name="index"),
    path('view', views.coba, name="index"),
    path('bacapres/create', views.create_bacapres, name="create_bacapres"),
    # path('bacapres/create2', views.BacapresCreateView.as_view(), name="create_bacapres2"),
    path('bacapres', views.bacapres_list, name="bacapres_list"),
    path('bacapres/edit/<int:id>', views.edit_bacapres, name="edit_bacapres"),
    # path('bacapres/delete/<int:pk>', views.create_bacapres, name="bacapres"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)