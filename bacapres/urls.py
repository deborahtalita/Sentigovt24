from django.urls import path
from . import views

app_name='bacapres'

urlpatterns = [
    path('', views.BacapresView.as_view(), name="bacapres_list"),
    path('create', views.BacapresCreateView.as_view(), name="create_bacapres"),
    path('edit/<int:id>', views.BacapresDetailView.as_view(), name="edit_bacapres"),
    path('delete/<int:id>', views.BacapresView.as_view(), name="delete_bacapres"),
]