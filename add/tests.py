from django.test import TestCase

# Create your tests here.


# import json
# import requests
# data={"number1":13 , "number2":12}
# json_data=json.dumps({"number1":12.5 , "number2":13})
# response = requests.post(url="http://127.0.0.1:8000/math/add",data=json_data)
# print(response.json())



from decimal import Decimal


a="12.1"
b="13.2"
print(Decimal(a)+Decimal(b))
