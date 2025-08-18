from django.db.models import F
from django.shortcuts import render
from .models import CartItem, ShoppingCart, Purchase, PurchaseItem, Product


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

