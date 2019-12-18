from django.contrib import admin
from django.urls import path, re_path, register_converter, converters
from . import views


urlpatterns = [
    path('show_basket', views.get_basket.as_view(), name="show_basket"),
    re_path('^product/(?P<id>\d+)$',views.ProductDetailView.as_view() , name = "product_detail")
    # re_path('add/(?P<number1>\-?\d+\.?\d*)/(?P<number2>\-?\d+\.?\d*)', views.Add.as_view(), name="add3"),

]
