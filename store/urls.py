from django.contrib import admin
from django.urls import path, re_path, register_converter, converters
from . import views


urlpatterns = [
    path('show_basket', views.get_basket.as_view(), name="add1"),

]
