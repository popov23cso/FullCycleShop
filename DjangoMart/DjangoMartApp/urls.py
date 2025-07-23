from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout_view'),
    path('category/<str:category_slug>', views.category_view, name='category'),
    path('cart', views.cart_view, name='cart'),
    path('product/<str:product_id>', views.product_view, name='product')
]