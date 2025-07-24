from .models import Category, ShoppingCart

def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }


def cart_processor(request):
    if request.user.is_authenticated:
        try:
            cart = ShoppingCart.objects.get(user_id=request.user)
        except ShoppingCart.DoesNotExist:
            cart = None
    else:
        cart = None

    return {'shopping_cart': cart}