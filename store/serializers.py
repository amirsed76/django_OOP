from rest_framework import serializers
from . import models
from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username',)


class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = '__all__'



class BasketSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    paymentStatus = serializers.CharField(read_only=True)
    trackingCode = serializers.CharField(read_only=True)
    payTime = serializers.DateTimeField(read_only=True)
    products_status_summary=serializers.SerializerMethodField("get_summary")
    class Meta:

        model = models.Basket
        # fields = ["customer","paymentStatus","recordTime","trackingCode","payTime"]
        fields="__all__"

    def get_summary(self,obj):
        basket_products = models.BasketProduct.objects.filter(basket = obj.id)
        result = "se"
        deliver_flag = True
        for product in basket_products:
            if product.state == "pr":
                result="pr"
            if product.state != "de":
                deliver_flag=False
        if deliver_flag :
            result="de"

        return  result



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields='__all__'


class BasketProductSerializer(serializers.ModelSerializer):
    state=serializers.CharField(read_only=True)
    class Meta:
        model = models.BasketProduct
        fields = ("id",'basket','product','count','state')

class SalesmanProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = ['profileImage']


class SalesmanIdentificationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = ['identificationImage']

class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model= models.Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta :
        model= models.Comment
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta :
        model= models.Color
        fields = '__all__'


class BasketProductInDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = models.BasketProduct
        fields = '__all__'


class BasketInDetailSerializer(serializers.ModelSerializer):
    products = BasketProductInDetailSerializer(many=True)
    class Meta:
        model = models.Basket
        fields = '__all__'