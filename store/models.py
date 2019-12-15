from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return '({}, {})'.format(self.username, self.email)


class Customer(User):
    pass     


class Salesman(User):
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=12)
    activity_description = models.TextField()
    activity_fields = models.CharField(max_length=300) # ???
    approved = models.BooleanField()
    location = models.CharField(max_length=300)
    profile_image = models.ImageField(upload_to='salesman_profile', blank=True)
    identification_image = models.ImageField(upload_to='salesman_identification_image', blank=True)
    registration_time = models.DateTimeField(auto_now_add=True) # ???
    suspend = models.BooleanField()


class Basket(models.Model):
    STATE_CHOICES = [
        ('pr', 'processing'),
        ('se', 'sending'),
        ('de', 'delivered')
    ]

    customer = models.ForeignKey(Customer , on_delete=models.CASCADE, related_name='baskets')
    payment_status = models.CharField(max_length=2, choices=STATE_CHOICES, default='pr')
    pay_time = models.DateTimeField()
    record_time = models.DateTimeField(auto_now_add=True) # ???
    tracking_code = models.CharField(max_length=300)


class Color(models.Model):
    name = models.CharField(max_length=10, primary_key=True)


class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class Product(models.Model):
    name = models.CharField(max_length=300)
    Price = models.IntegerField()
    salesman = models.ForeignKey(Salesman , on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products' , null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='products' , null=True)
    count = models.IntegerField()
    description = models.TextField()
    is_stock = models.BooleanField(default=False)
    record_time = models.DateTimeField(auto_now_add=True) # ???
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_content = models.ImageField(upload_to='product', blank=True)


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    count = models.IntegerField()
    state = models.CharField(max_length=20) # ???


