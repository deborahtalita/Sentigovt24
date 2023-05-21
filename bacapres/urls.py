from django.urls import path
from . import views

app_name='bacapres'

urlpatterns = [
    path('', views.bacapres_list, name="bacapres_list"),
    path('create', views.create_bacapres, name="create_bacapres"),
    path('edit/<int:id>', views.edit_bacapres, name="edit_bacapres"),
    path('delete/<int:id>', views.delete_bacapres, name="delete_bacapres"),
]