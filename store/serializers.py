from rest_framework import serializers
from . import models


class UserrSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
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

