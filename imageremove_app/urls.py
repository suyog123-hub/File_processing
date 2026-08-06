# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.remove_bg, name='remove_bg'),
    path('result/<int:pk>/', views.result, name='result'),
    path('download/<int:pk>/', views.download, name='download'),
    path('my-images/', views.my_images, name='my_images'),  # ← New
]