from django.contrib import admin
from django.urls import path, re_path, register_converter, converters
from . import views


urlpatterns = [
    path('add/', views.Add.as_view() , name="add1"),
    re_path('add/(?P<number1>\-?\d+\.?\d*)/(?P<number2>\-?\d+\.?\d*)',views.Add.as_view() , name="add3"),
    re_path('add/(?P<number1>\-?\d+\.?\d*)', views.Add.as_view(), name="add2"),

]
