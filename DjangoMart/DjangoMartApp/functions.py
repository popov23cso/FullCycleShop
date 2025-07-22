from django.db.models import F
from django.shortcuts import render


def add_product_to_cart(cart, product, qty=1):
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': qty}
    )
    if not created:
        cart_item.quantity = F('quantity') + qty
        cart_item.save()
        cart_item.refresh_from_db()
    return cart_item


def render_django_mart_app(request, template_name, context=None):
    if context is None:
        context = {}
    full_template_name = f'DjangoMartApp/{template_name}.html'
    return render(request, full_template_name, context)