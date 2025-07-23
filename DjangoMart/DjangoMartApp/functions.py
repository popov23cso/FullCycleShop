from django.db.models import F
from django.shortcuts import render
from .models import CartItem, ShoppingCart, Purchase, PurchaseItem, Product


def add_product_to_cart(cart, product, quantity):
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity = F('quantity') + quantity
        cart_item.save()
        cart_item.refresh_from_db()
    return cart_item

def product_has_enough_stock(product_id, quantity):
    product = Product.objects.get(id=product_id)
    if quantity <= product.stock:
        return True 
    return False


def render_django_mart_app(request, template_name, context=None):
    if context is None:
        context = {}
    full_template_name = f'DjangoMartApp/{template_name}.html'
    return render(request, full_template_name, context)

def create_user_purchase(user):
    cart = ShoppingCart.objects.get(user_id=user)
    cart_items = cart.cart_items.all().select_related('product')

    purchase = Purchase.objects.create(
                    user=user,
                    total_price=calculate_total_cart_price(cart_items)
                )

    for item in cart_items:
        PurchaseItem.objects.create(
            purchase=purchase,
            product_name=item.product.name,
            price_at_purchase=item.product.price,
            quantity=item.quantity
        )

    cart_items.delete()

def calculate_total_cart_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item.product.price
    
    return total_price