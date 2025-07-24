from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Category, Product, ShoppingCart, CartItem
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .functions import render_django_mart_app, product_has_enough_stock, add_product_to_cart
from django.core.exceptions import ObjectDoesNotExist
from markdown import markdown
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json 

# Create your views here.
def homepage_view(request):
    return render_django_mart_app(request, 'homepage')

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Paginator(Product.objects.filter(categories=category).order_by('-sales_count'), 20)
    page_number = request.GET.get('page')
    products_page = products.get_page(page_number)
    return render_django_mart_app(request, 'category', {'products':products_page})

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.description_html = markdown(product.description)
    return render_django_mart_app(request, 'product', {'product':product})

@login_required
@require_http_methods(["PUT"])
def add_to_cart(request):
    try:
        request_body = json.loads(request.body)
        product_id = request_body.get('product_id')
        quantity = request_body.get('quantity')
        if not product_id or not quantity:
            return JsonResponse({'error': 'Missing product_id or quantity'}, status=400)

        quantity = int(quantity)
        product = Product.objects.get(id=product_id)

        if product_has_enough_stock(product, quantity):
            add_product_to_cart(request.user, product, quantity) 
            return JsonResponse({'message': 'Product added successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Requested quantity exceeds our stock'}, status=409)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
@login_required
@require_http_methods(["PUT"])
def remove_from_cart(request):
    try:
        request_body = json.loads(request.body)
        item_id = request_body.get('cart_item_id')
        
        cart_item = CartItem.objects.get(id=item_id)
        cart = ShoppingCart.objects.get(user_id=request.user)

        if cart_item.cart != cart:
            return JsonResponse({'error': 'You can only manipulate your own cart!'}, status=403)

        cart.total_items_count -= cart_item.quantity
        cart_item.delete()

        cart.save()

        return JsonResponse({'message': 'Succesfully removed item from cart'}, status=404)

    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)


@login_required
def cart_view(request):
    cart, created = ShoppingCart.objects.get_or_create(user_id=request.user)
    cart_items = None
    total_cart_value = 0
    if not created:
        cart_items = cart.cart_items.select_related('product')
        total_cart_value = cart.total_value()

    return render_django_mart_app(request, 'cart', {
        'cart_items': cart_items,
        'total_cart_value':total_cart_value})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            return render_django_mart_app(request, 'login', {'error': 'Please input both email and password'})
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                login(request, user)
                return redirect('homepage')
        except User.DoesNotExist:
            pass

        return render_django_mart_app(request, 'login', {'error': 'Invalid username or password'})

    else:
        return render_django_mart_app(request, 'login')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        password_repeated = request.POST.get('repeatedPassword')

        if not email or not first_name or not last_name or not phone_number or not password or not password_repeated:
            return render_django_mart_app(request, 'register', {'error': 'Please fill out all required fields!'})
        if password != password_repeated:
            return render_django_mart_app(request, 'register', {'error': 'Passwords must match!'})
        
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number
            )
            user.set_password(password)
            user.save()
            login(request, user)
        except IntegrityError:
            return  render_django_mart_app(request, 'register', {'error': 'Email already taken!'})
        return redirect('homepage')

    else:
        return render_django_mart_app(request, 'register')
    
def logout_view(request):
    logout(request)
    return redirect('homepage')