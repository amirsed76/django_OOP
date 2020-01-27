
from rest_framework import routers
from . import views
from django.urls import path, include,re_path


router = routers.DefaultRouter()

router.register(r'basketproducts', views.BasketProductViewSet)
router.register(r'baskets', views.BasketViewSet)
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('confirm_basket/',views.confirm_basket,name="confirm_basket"),
    path('purchase/',views.purchase,name="purchase"),
    # path('my-basket/', views.MyBasketView.as_view()),
    # path('basket_products/<int:pk>/', views.BasketProductDetail.as_view(), name='basketproduct-detail'),
    path('categories/', views.GetCategories.as_view(), name="category"),
    path('products/<int:pk>/images/',views.ProductImages.as_view(),name="product_images"),
    path('product_images/', views.ProductImageList.as_view()),
    path('salesmans/', views.SalesmanList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('product_images/<int:pk>/', views.ProductImageDetail.as_view()),
    path('salesmans/<int:pk>/', views.SalesmanDetail.as_view()),
    # path('products/<int:pk>/pics/',views.ProductDetail.as_view(),name="product_images"),
    # path("products/" , views.ProductView)

]
