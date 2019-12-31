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
        fields = ('username', 'email')
        read_only_fields = ('username',)


class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Basket
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        # fields = ['id', 'imageContent']
        fields='__all__'


class BasketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasketProduct
        fields = '__all__'


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
