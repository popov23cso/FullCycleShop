from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Category, Product
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .functions import render_django_mart_app

# Create your views here.
def homepage(request):
    return render_django_mart_app(request, 'homepage')

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    top_products = Product.objects.filter(categories=category).order_by('-sales_count')[:20]

    return render_django_mart_app(request, 'category', {'top_products':top_products})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(username=email)
        password = request.POST['password']
        if user.check_password(password):
            login(request, user)
        else:
            return render_django_mart_app(request, 'login', {'error': 'Incorrect password!'})
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