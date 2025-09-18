from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    total_purchased_amount = models.FloatField(default=0)
    available_tokens = models.FloatField(default=500,  validators=[MinValueValidator(0)])
    delivery_details_provided_count = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(3)])
    is_deleted = models.BooleanField(default=False)

    # users who are approved are assigned this permission by admins
    is_api_user = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
    
class DeliveryDestination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)

class DeliveryTracking(models.Model):
    class Status(models.TextChoices):
        COLLECTING = 'Collecting'
        PREPARED = 'Prepared'
        SHIPPED = 'Shipped'
        DELIVERED = 'Delivered'
        CANCELLED = 'Cancelled'

    delivery_destination = models.ForeignKey(DeliveryDestination,
                                            on_delete=models.SET_NULL, 
                                            null=True,
                                            blank=True,
                                            related_name='delivery_tracking')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COLLECTING,
    )
    purchase = models.OneToOneField('Purchase', 
                                 on_delete=models.DO_NOTHING,
                                 related_name='delivery_tracking')
    created_date = models.DateTimeField(auto_now_add=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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
    is_active = models.BooleanField(default=True)

    # validate that a parent category does not have a parent itself
    def save(self, *args, **kwargs):
        if self.parent_category and self.is_main_category:
            raise ValueError("Main categories shouldn't have a parent.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

class Brand(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title}'

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    price = models.FloatField(validators=[MinValueValidator(1.0)])
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    product_weight = models.CharField(max_length=50, blank=True, null=True)
    product_height = models.CharField(max_length=50, blank=True, null=True)
    product_width = models.CharField(max_length=50, blank=True, null=True)
    product_length = models.CharField(max_length=50, blank=True, null=True)
    package_weight = models.CharField(max_length=50, blank=True, null=True)
    package_height = models.CharField(max_length=50, blank=True, null=True)
    package_width = models.CharField(max_length=50, blank=True, null=True)
    package_length = models.CharField(max_length=50, blank=True, null=True)
    warranty = models.PositiveIntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'
    
    @property
    def average_rating(self):

        # get all related reviews through purchase items
        reviews = Review.objects.filter(purchase_item__product_id=self.id)
        return reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0.0

class ShoppingCart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    total_items_count = models.PositiveIntegerField(default=0)
    def total_value(self):
        cart_items = self.cart_items.select_related('product')
        return sum(item.quantity * item.product.price for item in cart_items)
    def empty_cart(self):
        self.cart_items.all().delete()
        self.total_items_count = 0
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total_price = models.FloatField()
    is_invalid = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING, related_name='purchase_items')
    product_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                related_name='purchase_item',
                                blank=True,
                                null=True)
    price_at_purchase = models.FloatField()
    quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_item = models.OneToOneField('PurchaseItem', on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        # run model validation before saving
        self.full_clean()  
        super().save(*args, **kwargs)