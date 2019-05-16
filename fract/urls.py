from django.urls import path
from .views import ImageListView, ImageDetailView
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', ImageListView.as_view(), name='index'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image'),
    
]