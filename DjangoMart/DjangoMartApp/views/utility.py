from django.db.models import F
from django.shortcuts import render
from ..models import CartItem, ShoppingCart, Purchase
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__" 

class ApiPagination(PageNumberPagination):
    page_size = 50

    # the users can pass ?page_size=X (X<=100) to get more results per page 
    page_size_query_param = "page_size" 
    max_page_size = 100

def add_product_to_cart(user, product, quantity):
    cart, created = ShoppingCart.objects.get_or_create(user_id=user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity = F('quantity') + quantity
        cart_item.save()
    cart.total_items_count += quantity
    cart.save()
    
def product_has_enough_stock(product, quantity):
    if quantity <= product.stock:
        return True 
    return False

def render_django_mart_app(request, template_name, context=None):
    if context is None:
        context = {}
    full_template_name = f'DjangoMartApp/{template_name}.html'
    return render(request, full_template_name, context)

def parse_date(date):
    try:
        return datetime.fromisoformat(date)
    except (TypeError, ValueError):
        return None

