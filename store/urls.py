from django.contrib import admin
from django.urls import path, re_path, register_converter, converters
from . import views


urlpatterns = [
    path('show_basket', views.get_basket.as_view(), name="show_basket"),
    re_path('^product/(?P<id>\d+)$',views.ProductDetailView.as_view() , name = "product_detail"),
    re_path('^product/(?P<id>\d+)/images$',views.ProductImages.as_view() , name = "product_images"),
    path('search/<str:searched>/', views.search, name='search'),
    path('searching/<str:searched>/', views.searching, name='searching'),
    path('categoryProducts/<str:cat>/',views.showproducts,name="show_products"),
    path('deleteBasketItem/<int:itemID>',views.deleteBasketItem,name="deleteItem")
]
