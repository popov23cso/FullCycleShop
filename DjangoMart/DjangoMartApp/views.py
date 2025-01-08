from django.shortcuts import render, redirect
from .models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def homepage(request):
    return render(request, 'DjangoMartApp/homepage.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(username=email)
        password = request.POST['password']
        if user.check_password(password):
            login(request, user)
        else:
            return render(request, 'DjangoMartApp/login.html', {
                'error': 'Incorrect password!'
            })
        return redirect('homepage')

    else:
        return render(request, 'DjangoMartApp/login.html')

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
            return render(request, 'DjangoMartApp/register.html', {
                'error': 'Passwords must match!'
            })
        
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
            return render(request, 'pfitness/register.html', {
                'error': 'Email already taken!'
            })
        return redirect('homepage')

    else:
        return render(request, 'DjangoMartApp/register.html')
    
def logout_view(request):
    logout(request)
    return redirect('homepage')