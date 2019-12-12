from django.db import models
from django.contrib.auth.models import AbstractBaseUser

#AbstractBaseUser has password

class Costumer(AbstractBaseUser):
    Username = models.CharField(max_length=50)

class SalesMan(AbstractBaseUser):
    Username = models.CharField(max_length=50)
    ActivityDescription = models.TextField()
    ActivityFields = models.CharField(max_length=300)
    Approved = models.BooleanField()
    Email = models.EmailField()
    IdentificationImage = models.TextField()
    Location = models.CharField(max_length=300)
    Name = models.CharField(max_length=300)
    PhoneNumber = models.CharField(max_length=12)
    ProfileImage=models.TextField()
    RegistrationTime=models.DateTimeField()
    Suspend = models.BooleanField()


class Basket(models.Model):
    costumer = models.ForeignKey(Costumer , on_delete=models.CASCADE)
    PaymentStatus = models.CharField(max_length=50)
    PayTime = models.DateTimeField()
    RecordTime = models.DateTimeField()
    TrackingCode = models.CharField(max_length=300)

class Product(models.Model):
    SalesMan = models.ForeignKey(SalesMan , on_delete=models.CASCADE)
    Category = models.CharField(max_length=300)
    Color = models.CharField(max_length=50)
    Count = models.IntegerField()
    Description = models.TextField()
    isStock = models.BooleanField(default=False)
    Name = models.CharField(max_length=300)
    Price = models.IntegerField()
    RecordTime = models.DateTimeField()



class ProductImage(models.Model):
    ImageContent = models.ImageField()

class BasketProduct(models.Model):
    Count = models.IntegerField()
    State = models.CharField(max_length=50)
    Basket = models.ForeignKey(Basket , on_delete=models.CASCADE)
    Product = models.ForeignKey(Product , on_delete=models.CASCADE)

