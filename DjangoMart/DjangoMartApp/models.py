from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    total_purchased_amount = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_date = models.DateTimeField(auto_now=True)

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    is_main_category = models.BooleanField(default=False)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # validate that a parent category does not have a parent itself
    def save(self, *args, **kwargs):
        if self.parent_category and self.is_main_category:
            raise ValueError("Main categories shouldn't have a parent.")
        super().save(*args, **kwargs)

class Brand(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    price = models.FloatField(validators=[MinValueValidator(1.0)])
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    rating = models.FloatField(blank=True, null=True)
    rating_count = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category)
    product_weight = models.CharField(max_length=50, blank=True, null=True)
    product_height = models.CharField(max_length=50, blank=True, null=True)
    product_width = models.CharField(max_length=50, blank=True, null=True)
    product_length = models.CharField(max_length=50, blank=True, null=True)
    package_weight = models.CharField(max_length=50, blank=True, null=True)
    package_height = models.CharField(max_length=50, blank=True, null=True)
    package_width = models.CharField(max_length=50, blank=True, null=True)
    package_length = models.CharField(max_length=50, blank=True, null=True)
    warranty = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




