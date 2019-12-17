
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal

class get_basket(APIView):

    def get(self, request, *args, **kwargs):
            exist=True
            list1=[{"goods_id":13, "number":5 ,"sum":13000} , {"goods_id":14, "number":3 , "sum":75000}]

            # exist=False
            # list1=[]
            return Response({"exist":exist ,"content":list1})




