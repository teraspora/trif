from django.urls import path
from .views import ImageListView
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', ImageListView.as_view(), name='index'),
]