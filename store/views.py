from rest_framework.response import Response
from rest_framework.decorators import api_view
from itertools import chain
from rest_framework import pagination
from rest_auth.registration.views import RegisterView

from . import models
from . import serializers
from rest_framework import viewsets
from rest_framework import response
from rest_framework import status
from rest_framework import parsers
from rest_framework import decorators
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django.db import transaction
from rest_framework import mixins
import uuid
import random
import math



@api_view(['GET'])
def confirm_basket(request):
    user_basket=models.Basket.objects.get(customer=request.user , paymentStatus="pr")
    basket_products=models.BasketProduct.objects.filter(basket=user_basket,state="pr")

    products_serializer=serializers.BasketProductSerializer(basket_products,many=True)
    return Response(products_serializer.data)

@api_view(['POST'])
def purchase(request):
    rand=random.random()
    successfull=False
    if rand<.80:
        successfull=True
        tracking_code=math.floor(random.random()*1000000)
        user_basket=models.Basket.objects.get(customer=request.user , paymentStatus="pr")
        basket_products=models.BasketProduct.objects.filter(basket=user_basket,state="pr")
        for basket_product in basket_products:
            basket_product.product.count-=basket_product.count
            basket_product.product.save()
            
        user_basket.paymentStatus="co"
        user_basket.save()
        return Response({"successfull":successfull,"tracking_code":tracking_code})

    
    return Response({"successfull":successfull})


# class get_basket(APIView):
#     def get(self, request, *args, **kwargs):
#         exist = True
#         list1 = [{"goods_id": 13, "number": 5, "sum": 13000}, {"goods_id": 14, "number": 3, "sum": 75000}]
#
#         # exist=False
#         # list1=[]
#         return Response({"exist": exist, "content": list1})


# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#     lookup_field = 'id'

#
class ProductImages(generics.ListAPIView):
    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer

    def get(self, request, pk, *args, **kwargs):
        pics = models.ProductImage.objects.filter(product__id=pk)
        serializer = self.serializer_class(pics, many=True)
        return response.Response(serializer.data)


#
# @api_view(['GET'])
# def search(request, searched):
#     products = models.Product.objects.filter(
#         name__contains=searched).order_by('recordTime')[0:10]
#     serializer = serializers.ProductSerializer(products, many=True)
#     return Response(serializer.data)

#
# @api_view(['GET'])
# def searching(request, searched):
#     searched_length = len(searched)
#     products = models.Product.objects.filter(
#         name__contains=searched).order_by('recordTime')
#
#     for k in range(0, searched_length + 1):
#         products_length = len(products)
#
#         if products_length > 2:
#
#             serializer = serializers.ProductSerializer(products[0:2], many=True)
#             return Response(serializer.data)
#
#
#         else:
#             new_products = models.Product.objects.filter(
#                 name__contains=searched[0:searched_length - k - 1]).order_by('recordTime')
#             products = list(chain(products, new_products))

# @api_view(['GET'])
# def showproducts(request,cat):
#     paginator = pagination.PageNumberPagination()
#     paginator.page_size = 2
#     product_list=models.Product.objects.all().filter(category=cat)
#     result_page = paginator.paginate_queryset(product_list, request)
#     serializer = serializers.ProductSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)


# @api_view(['GET'])
# def deleteBasketItem(request,itemID):
#     item=models.BasketProduct.objects.get(pk=itemID)
#     item.count-=1
#     if item.count==0:
#         item.delete()
#         return Response({"item":"item deleted","delete":True})
#     else:
#         item.save()
#         serializer=models.BasketProductSerializer(item)
#         return Response({"item":serializer.data,"deleted":False})
#



class GetCategories(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CustomRegisterView(RegisterView):
    queryset = models.User.objects.all()


class ProductList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset


class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomUserDetailsSerializer
    queryset = models.Customer.objects.all()


class SalesmanDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializers.SalesmanSerializer
    queryset = models.Salesman.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SalesmanList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.SalesmanSerializer
    queryset = models.Salesman.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductImageList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImage.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductImageDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImage.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BasketProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasketProductSerializer
    queryset = models.BasketProduct.objects.all()

    def get_queryset(self):
        queryset = models.BasketProduct.objects.filter(basket__customer=self.request.user)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        product_id = request.data['product']
        product = models.Product.objects.filter(id=product_id)
        if not product:
            return response.Response({'message': 'product not found'}, status=status.HTTP_400_BAD_REQUEST)
        product = product[0]
        count = int(request.data['count'])
        if product.count < count:
            return response.Response({'message': 'product count exceeded'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class FinalPayment(APIView):
    def put(self, request, *args, **kwargs):
        basket = models.Basket.objects.filter(customer=request.user)
        basket.paymentStatus = "co"
        basket.trackingCode = uuid.uuid1()
        basket.save()
        return response


class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasketSerializer
    queryset  = models.Basket.objects.all()

    def get_queryset(self):
        queryset = models.Basket.objects.filter(customer=self.request.user)
        return queryset
