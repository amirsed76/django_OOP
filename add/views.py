
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal

class Add(APIView):

    def get(self, request, *args, **kwargs):
        try:
            nums = request.GET
            sum = Decimal('0')
            if(len(nums) >= 1):
                for i in nums:
                    sum += Decimal(nums[i])
                return Response({'result': sum})

            elif "number1" in kwargs.keys() :
                if "number2" in kwargs.keys():
                    sum = Decimal(kwargs["number1"])+Decimal(kwargs["number2"])
                    return Response({'result': sum})
                else:
                    return Response({'result':Decimal(kwargs["number1"])})

            else:
                return Response({"content":'you should enter at least one number.'})
        except:
            return Response({"content":"there is an error"})

    def post(self, request, format=None):
        try:
            sum = Decimal(0)
            nums=request.data
            if (len(nums) >= 1):
                for i in nums:
                    sum += Decimal(str(nums[i]))
                return Response({'result': sum})
        except:
            return Response({"content":"there is an error"})


