from django.contrib.auth.models import AbstractUser
from django.db import models
from adminDashboard.models import Product

class MyUser(AbstractUser):
    profilePic = models.IntegerField(null=True, blank=True)
    cart = models.ManyToManyField(Product, through='MyUserProduct',blank=True,)

class MyUserProduct(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
