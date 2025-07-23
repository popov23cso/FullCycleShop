from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Category, Product, ShoppingCart, CartItem
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .functions import render_django_mart_app
from django.core.exceptions import ObjectDoesNotExist
from markdown import markdown

# Create your views here.
def homepage(request):
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


def cart_view(request):
    cart, created = ShoppingCart.objects.get_or_create(user_id=request.user)
    cart_items = None
    if not created:
        cart_items = cart.cart_items.select_related('product')

    return render_django_mart_app(request, 'cart', {'cart_items': cart_items})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return render_django_mart_app(request, 'login', {'error': 'Invalid username or password'})
        password = request.POST['password']
        if user.check_password(password):
            login(request, user)
        else:
            return render_django_mart_app(request, 'login', {'error': 'Invalid username or password'})
        return redirect('homepage')

    else:
        return render_django_mart_app(request, 'login')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['firstName']
        middle_name = request.POST['middleName']
        last_name = request.POST['lastName']
        phone_number = request.POST['phoneNumber']
        represented_company_name = request.POST['representedCompanyName']

        password = request.POST['password']
        password_repeated = request.POST['repeatedPassword']

        if password != password_repeated:
            return render_django_mart_app(request, 'register', {'error': 'Passwords must match!'})
        
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                phone_number=phone_number,
                represented_company_name=represented_company_name
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