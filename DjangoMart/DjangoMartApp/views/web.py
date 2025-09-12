from ..models import (User, Category, Product, ShoppingCart,
                    CartItem, DeliveryDestination, Purchase, 
                    PurchaseItem, DeliveryTracking)

from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django.contrib.auth import login, logout
from .utility import render_django_mart_app, product_has_enough_stock
from markdown import markdown
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage_view(request):
    return render_django_mart_app(request, 'homepage')

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Paginator(Product.objects.filter(categories=category, is_active=True).order_by('-sales_count'), 20)
    page_number = request.GET.get('page')
    products_page = products.get_page(page_number)
    return render_django_mart_app(request, 'category', {'products':products_page})

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.description_html = markdown(product.description)
    return render_django_mart_app(request, 'product', {'product':product})

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

@login_required
def checkout(request):
    if request.method == 'GET':

        delivery_destinations = DeliveryDestination.objects.filter(user=request.user)
        available_tokens = request.user.available_tokens
        cart = ShoppingCart.objects.get(user_id=request.user)
        cart_total_value = cart.total_value()

        delivery_details_provided_count = request.user.delivery_details_provided_count
        balance_after_purchase = available_tokens - cart_total_value
        can_afford_cart = balance_after_purchase >= 0

        return render_django_mart_app(request, 'checkout', {
            'available_tokens': available_tokens,
            'cart_total_value': cart_total_value,
            'delivery_destinations': delivery_destinations,
            'delivery_details_provided_count': delivery_details_provided_count,
            'can_afford_cart': can_afford_cart,
            'balance_after_purchase': balance_after_purchase
        })
    
    elif request.method == 'POST':
        # if anything fails roll back all changes
        with transaction.atomic():
            address_id = request.POST.get('addressID')
            cart = ShoppingCart.objects.select_for_update().get(user_id=request.user)
            total_value = cart.total_value()
            if total_value > request.user.available_tokens:
                return render_django_mart_app(request, 'error', {'message':'Insufficient tokens to complete transaction'})

            cart_items = cart.cart_items.select_related('product').select_for_update(of=('product',))
            purchase = Purchase.objects.create(user=request.user, total_price=total_value)

            for item in cart_items:
                if not product_has_enough_stock(item.product, item.quantity):
                    return render_django_mart_app(request,'error', {'message': 
                                                                    f"Product {item.product.title} has insufficient stock: " +
                                                                    f"\n{item.quantity} in cart, {item.product.stock} in stock"})
            purchase_items = [
                PurchaseItem(
                    purchase=purchase,
                    product_name=item.product.title,
                    product_id=item.product.id,
                    price_at_purchase=item.product.price,
                    quantity=item.quantity)
                for item in cart_items
            ]

            PurchaseItem.objects.bulk_create(purchase_items)

            try:
                delivery_destination = DeliveryDestination.objects.get(id=address_id, user=request.user)
            except DeliveryDestination.DoesNotExist:
                return render_django_mart_app(request, 'error', {'message':'The requested address does not exist for this user'})

            DeliveryTracking.objects.create(user=request.user,
                                            delivery_destination=delivery_destination,
                                            city=delivery_destination.city,
                                            street=delivery_destination.street,
                                            street_number=delivery_destination.street_number,
                                            phone_number=delivery_destination.phone_number,
                                            status=DeliveryTracking.Status.COLLECTING,
                                            purchase=purchase)
            
            cart.empty_cart()
            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.sales_count += item.quantity
            Product.objects.bulk_update([item.product for item in cart_items], ['stock'])

            request.user.total_purchased_amount += total_value
            request.user.available_tokens -= total_value
            request.user.save()
            return redirect('orders')

    
@login_required
def orders(request):
    deliveries = DeliveryTracking.objects.filter(user=request.user).order_by('-created_date')
    return render_django_mart_app(request, 'orders', {'deliveries':deliveries})

@login_required
def delivery(request, delivery_id):
    try:
        delivery = (DeliveryTracking.objects
                    .select_related('purchase')
                    .prefetch_related('purchase__purchase_items')
                    .get(user=request.user, id=delivery_id))
    except DeliveryTracking.DoesNotExist:
        return render_django_mart_app(request, 'error', {'message':'The requested delivery does not exist for this user'})
    return render_django_mart_app(request, 'delivery', {'delivery':delivery})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
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