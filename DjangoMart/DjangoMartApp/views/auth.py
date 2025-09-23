from ..models import User
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth import login, logout
from .utility import render_django_mart_app

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([email, password]):
            return render_django_mart_app(request, 'login', {'message': 'Please input both email and password'})
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                login(request, user)
                return redirect('homepage')
        except User.DoesNotExist:
            pass

        return render_django_mart_app(request, 'login', {'message': 'Invalid username or password'})

    else:
        return render_django_mart_app(request, 'login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        password_repeated = request.POST.get('repeatedPassword')

        if not all([email, first_name, last_name, phone_number, password, password_repeated]):
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