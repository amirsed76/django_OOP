from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from itertools import chain
from rest_framework import pagination
from rest_auth.registration.views import RegisterView
import datetime
from . import models
from .models import Salesman, Basket, BasketProduct
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
from rest_auth.views import LoginView
from rest_framework import permissions
from . import permission


class CustomerLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        keep = request.data.get('keep', None)
        if not keep:
            request.session.set_expiry(0)

        return super().post(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def purchase_list(request):
    completed_baskets = Basket.objects.filter(customer=request.user, paymentStatus="co")
    basket_products = BasketProduct.objects.filter(basket__in=completed_baskets)
    basket_product_serializer = serializers.BasketProductSerializer(basket_products, many=True)
    return Response(basket_product_serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def confirm_basket(request):
    user_basket = models.Basket.objects.get(customer=request.user, paymentStatus="pr")
    basket_products = models.BasketProduct.objects.filter(basket=user_basket, state="pr")

    products_serializer = serializers.BasketProductSerializer(basket_products, many=True)
    return Response(products_serializer.data)


@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated])
def purchase(request):
    try:
        user_basket = models.Basket.objects.get(customer=request.user, paymentStatus="pr")
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    basket_products = models.BasketProduct.objects.filter(basket=user_basket, state="pr")
    if request.method == 'GET':
        total_price = 0
        for basket_product in basket_products:
            total_price += basket_product.count * basket_product.product.Price

        return Response({"total_price": total_price})

    rand = random.random()
    successfull = False
    if rand < .80:
        successfull = True
        tracking_code = math.floor(random.random() * 1000000)
        for basket_product in basket_products:
            basket_product.product.count -= basket_product.count
            basket_product.product.save()

        user_basket.paymentStatus = "co"
        user_basket.trackingCode = tracking_code
        user_basket.payTime = datetime.datetime.now()
        user_basket.save()
        return Response({"successfull": successfull, "tracking_code": tracking_code})

    return Response({"successfull": successfull}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def communicate_seller(request, id):
    seller = Salesman.objects.get(id=id)
    salesman_serializer = serializers.SalesmanSerializer(seller)
    return Response(salesman_serializer.data)


class ProductImages(generics.ListAPIView):
    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer

    def get(self, request, pk, *args, **kwargs):
        pics = models.ProductImage.objects.filter(product__id=pk)
        serializer = self.serializer_class(pics, many=True)
        return response.Response(serializer.data)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.BasketProduct.objects.filter(basket__customer=self.request.user)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        product_id = request.data['product']
        product = models.Product.objects.filter(id=product_id)
        if not product:
            return response.Response({'message': 'product not found'}, status=status.HTTP_400_BAD_REQUEST)
        product = product[0]
        count = int(request.data['count'])
        if product.count < count:
            return response.Response({'message': 'product count exceeded'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['basket'] = models.Basket.objects.get(customer=request.user, paymentStatus='pr').pk
        request.data._mutable = _mutable

        return super().create(request, *args, **kwargs)


class FinalPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        basket = models.Basket.objects.filter(customer=request.user)
        basket.paymentStatus = "co"
        basket.trackingCode = uuid.uuid1()
        basket.save()
        return response


class LastBasketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasketSerializer
    queryset = models.Basket.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Basket.objects.filter(customer=self.request.user, paymentStatus='pr')

    def create(self, request, *args, **kwargs):
        if len(self.get_queryset()) > 0:
            return Response({'message': 'can not create another processing basket'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['customer'] = request.user.id
        request.data['paymentStatus'] = 'pr'
        return super().create(request, *args, **kwargs)


class BasketView(generics.ListAPIView):
    serializer_class = serializers.BasketSerializer
    queryset = models.Basket.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.Basket.objects.filter(customer=self.request.user, paymentStatus='co')
        return queryset


class LoggedIn(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class MyComments(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get_queryset(self):
        queryset = models.Comment.objects.filter(customer=self.request.user)
        return queryset


class MyComment(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get_queryset(self):
        queryset = models.Comment.objects.filter(customer=self.request.user)
        return queryset


class CreateComment(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True

        product_id = request.data["product"]
        basket_products = models.BasketProduct.objects.filter(basket__customer=request.user, product=product_id)
        if len(basket_products) > 0:
            request.data['customer'] = request.user.id
            request.data._mutable = _mutable 
            return super().post(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class productComments(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get(self, request, product, *args, **kwargs):
        data = models.Comment.objects.filter(product=product)
        serializer_data = serializers.CommentSerializer(data, many=True)

        return Response(serializer_data.data)


class GetColors(generics.ListAPIView):
    queryset = models.Color.objects.all()
    serializer_class = serializers.ColorSerializer