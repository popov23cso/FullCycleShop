from django.urls import path

from .views.web import (homepage_view, login_view, register,
                    logout_view, category_view, cart_view,
                    product_view, checkout, orders,
                    delivery )

from .views.api import (add_to_cart, remove_from_cart, add_address,
                    remove_address, get_purchases, CustomTokenObtainPairView,
                    get_purchase_items, get_products, get_users)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    # Webpage views
    path('', homepage_view, name='homepage'),
    path('login', login_view, name='login_view'),
    path('register', register, name='register'),
    path('logout', logout_view, name='logout_view'),
    path('category/<str:category_slug>', category_view, name='category'),
    path('cart', cart_view, name='cart'),
    path('product/<int:product_id>', product_view, name='product'),
    path('checkout', checkout, name='checkout'),
    path('orders', orders, name='orders'),
    path('delivery/<int:delivery_id>', delivery, name='delivery'),

    # API`s
    path('add_to_cart', add_to_cart, name='add_to_cart'),
    path('remove_from_cart', remove_from_cart, name='remove_from_cart'),
    path('add_address', add_address, name='add_address'),
    path('remove_address', remove_address, name='remove_address'),
    path('get_purchases', get_purchases, name='get_purchases'),
    path('get_purchase_items', get_purchase_items, name='get_purchase_items'),
    path('get_products', get_products, name='get_products'),
    path('get_users', get_users, name='get_users'),

    # Token based authentication
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]