from django.urls import path

from . import views


app_name = 'sentiment'

urlpatterns = [
    path('crawl', views.crawl, name="index"),
    path('scrape', views.scrape, name="index"),
    path('bacapres/create', views.create_bacapres, name="create_bacapres"),
    path('bacapres', views.bacapres_list, name="bacapres_list"),
    path('bacapres/edit/<int:id>', views.edit_bacapres, name="edit_bacapres"),
    # path('bacapres/delete/<int:pk>', views.create_bacapres, name="bacapres"),
]