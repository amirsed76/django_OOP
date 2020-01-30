
from rest_framework import routers
from . import views
from django.urls import path, include,re_path


router = routers.DefaultRouter()

router.register(r'basketproducts', views.BasketProductViewSet)
router.register(r'last_basket', views.LastBasketViewSet)
# router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('confirm_basket/',views.confirm_basket,name="confirm_basket"),
    path('purchase/',views.purchase,name="purchase"),
    path('categories/', views.GetCategories.as_view(), name="category"),
    path('products/<int:pk>/images/',views.ProductImages.as_view(),name="product_images"),
    path('product_images/', views.ProductImageList.as_view()),
    path('salesmans/', views.SalesmanList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('product_images/<int:pk>/', views.ProductImageDetail.as_view()),
    path('salesmans/<int:pk>/', views.SalesmanDetail.as_view()),
    path('login/', views.CustomerLoginView.as_view()),
    path('communicate_seller/<int:id>',views.communicate_seller,name="communicate_seller"),
    path('purchase_list/',views.purchase_list,name='purchase_list'),
    path('logged-in/', views.LoggedIn.as_view()),
    path("baskets/",views.BasketView.as_view()),
    path('my_comment/', views.MyComments.as_view()),
    path('my_comment/<int:pk>/', views.MyComment.as_view()),
    path('create_comment/', views.CreateComment.as_view()),
    path('product-comment/<int:product>/', views.productComments.as_view()),
    path('colors/', views.GetColors.as_view(), name="color"),
    path('last-basket/', views.LastBasketListProducts.as_view()),
]
