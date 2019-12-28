from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import datetime


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


class Customer(User):
    class Meta:
        verbose_name = 'customer'


class Salesman(User):
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=12)
    activityDescription = models.TextField(blank=True , null=True)
    approved = models.BooleanField(blank=True , null=True)
    profileImage = models.ImageField(upload_to='salesman_profile', blank=True , null= True)
    identificationImage = models.ImageField(upload_to='salesman_identification_image', blank=True , null=True)
    suspend = models.BooleanField(default=False)
    activityFields = models.CharField(max_length=300 , null=True , blank=True)
    location = models.CharField(max_length=300)
    registrationTime = models.DateField()

    class Meta:
        verbose_name = 'salesman'

    def __str__(self):
        return '({}, {})'.format(self.username, self.email)


class Basket(models.Model):
    STATE_CHOICES = [
        ('pr', 'processing'),
        ('co', 'Completed'),
    ]

    customer = models.ForeignKey(Customer , on_delete=models.CASCADE, related_name='baskets')
    paymentStatus = models.CharField(max_length=2, choices=STATE_CHOICES, default='pr')
    recordTime = models.DateTimeField(auto_now_add=True )
    trackingCode = models.CharField(max_length=300, null=True , blank=True)
    payTime = models.DateTimeField( null=True , blank=True)

    def __str__(self):
        return self.customer.username + "-" + self.paymentStatus


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name    


class Product(models.Model):
    name = models.CharField(max_length=300)
    count = models.IntegerField()
    description = models.TextField(blank=True , null=True)
    isStock = models.BooleanField(default=False)
    Price = models.IntegerField()
    salesman = models.ForeignKey(Salesman , on_delete=models.CASCADE, related_name='products')
    recordTime = models.DateTimeField(auto_now_add=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='color', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category', null=True)

    def __str__(self):
         return '({}, {})'.format(self.name , self.count)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    imageContent = models.ImageField(upload_to='product', blank=True , null=True)


class BasketProduct(models.Model):
    STATE_CHOICES = (
        ('pr', 'processing'),
        ('se', 'sending'),
        ('de', 'delivered')
    )
    basket = models.ForeignKey(Basket , on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    count = models.IntegerField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='pr')

    def __str__(self):
        return '({}, {} , {},{})'.format(self.product.name , self.basket.customer , self.count,self.basket)

