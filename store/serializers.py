from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['username', 'email']


class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = '__all__'


class SalesmanProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = ['profile_image']


class SalesmanIdentificationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salesman
        fields = ['identication_image']


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Basket
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'


class BasketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasketProduct
        fields = '__all__'