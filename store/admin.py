from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Customer)
admin.site.register(models.Salesman)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.BasketProduct)
admin.site.register(models.Basket)
admin.site.register(models.Color)
admin.site.register(models.Category)