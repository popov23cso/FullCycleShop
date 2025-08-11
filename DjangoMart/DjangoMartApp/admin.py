from django.contrib import admin

from .models import User, Category, Product, Brand, CartItem, ShoppingCart, DeliveryDestination, DeliveryTracking, Purchase, PurchaseItem

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(CartItem)
admin.site.register(ShoppingCart)
admin.site.register(DeliveryDestination)
admin.site.register(DeliveryTracking)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)