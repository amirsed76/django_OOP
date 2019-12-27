from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . import models
from . import serializers
from rest_framework.decorators import api_view
from itertools import chain
from rest_framework import pagination

class get_basket(APIView):
    def get(self, request, *args, **kwargs):
        exist = True
        list1 = [{"goods_id": 13, "number": 5, "sum": 13000}, {"goods_id": 14, "number": 3, "sum": 75000}]

        # exist=False
        # list1=[]
        return Response({"exist": exist, "content": list1})


class ProductDetailView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'id'


class ProductImages(generics.ListAPIView):
    queryset = models.ProductImage.objects.all()

    serializer_class = serializers.ProductImageSerializer
    lookup_field = "product__id"


@api_view(['GET'])
def search(request, searched):
    products = models.Product.objects.filter(
        name__contains=searched).order_by('recordTime')[0:10]
    serializer = serializers.ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searching(request, searched):
    searched_length = len(searched)
    products = models.Product.objects.filter(
        name__contains=searched).order_by('recordTime')

    for k in range(0, searched_length + 1):
        products_length = len(products)

        if products_length > 2:

            serializer = serializers.ProductSerializer(products[0:2], many=True)
            return Response(serializer.data)


        else:
            new_products = models.Product.objects.filter(
                name__contains=searched[0:searched_length - k - 1]).order_by('recordTime')
            products = list(chain(products, new_products))

@api_view(['GET'])
def showproducts(request,cat):
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 2
    product_list=models.Product.objects.all().filter(category=cat)
    result_page = paginator.paginate_queryset(product_list, request)
    serializer = serializers.ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def deleteBasketItem(request,itemID):
    item=BasketProduct.objects.get(pk=itemID)
    item.count-=1
    if item.count==0:
        item.delete()
        return Response({"item":"item deleted","delete":True})
    else:
        item.save()
        serializer=BasketProductSerializer(item)
        return Response({"item":serializer.data,"deleted":False})
