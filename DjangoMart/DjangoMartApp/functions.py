from django.db.models import F

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
