from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test, name="test"),
    path('home/', views.home, name="home"),
    path('', views.index, name="index"),
    path('<int:soption>', views.sindex, name="sindex"),
]
