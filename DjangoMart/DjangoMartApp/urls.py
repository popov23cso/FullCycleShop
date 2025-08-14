from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout_view'),
    path('category/<str:category_slug>', views.category_view, name='category'),
    path('cart', views.cart_view, name='cart'),
    path('product/<int:product_id>', views.product_view, name='product'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('add_address', views.add_address, name='add_address'),
    path('remove_address', views.remove_address, name='remove_address'),
    path('orders', views.orders, name='orders')
]