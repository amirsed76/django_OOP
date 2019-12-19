
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . import models
from . import serializers
class get_basket(APIView):

    def get(self, request, *args, **kwargs):
            exist=True
            list1=[{"goods_id":13, "number":5 ,"sum":13000} , {"goods_id":14, "number":3 , "sum":75000}]

            # exist=False
            # list1=[]
            return Response({"exist":exist ,"content":list1})



class ProductDetailView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'id'


class ProductImages(generics.ListAPIView):
    queryset = models.ProductImage.objects.all()

    serializer_class = serializers.ProductImageSerializer
    lookup_field = "product__id"


