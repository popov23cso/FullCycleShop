from django.db.models import F, QuerySet
from django.shortcuts import render
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .serializers import (PurchaseSerializer, PurchaseItemSerializer, ProductSerializer)
from ..models import (Product, ShoppingCart, CartItem, 
                      Purchase, PurchaseItem)


class ApiPagination(PageNumberPagination):
    page_size = 50

    # the users can pass ?page_size=X (X<=100) to get more results per page 
    page_size_query_param = "page_size" 
    max_page_size = 100

def add_product_to_cart(user, product, quantity):
    cart, created = ShoppingCart.objects.get_or_create(user_id=user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity = F('quantity') + quantity
        cart_item.save()
    cart.total_items_count += quantity
    cart.save()
    
def product_has_enough_stock(product, quantity):
    if quantity <= product.stock:
        return True 
    return False

def render_django_mart_app(request, template_name, context=None):
    if context is None:
        context = {}
    full_template_name = f'DjangoMartApp/{template_name}.html'
    return render(request, full_template_name, context)

def parse_date(date):
    try:
        return datetime.fromisoformat(date)
    except (TypeError, ValueError):
        return None

def validate_api_date_parameters(created_after, updated_after):
    created_after = parse_date(created_after)
    updated_after = parse_date(updated_after)

    validation_error = None
    if updated_after is not None and created_after is not None:
        validation_error =  'Created_after and updated_after cannot be passed at the same time'
    elif updated_after is None and created_after is None:
        validation_error =  'Supplying updated_after or created_after parameter is required. Passed dates need to be in valid ISO 8601 format'

    if validation_error is not None:
        validation_response = Response(
            {
                'success':False,
                'error': validation_error
            },
            status=status.HTTP_400_BAD_REQUEST)
        
        return False, validation_response, None
    
    filter_date = updated_after if updated_after is not None else created_after
    filter_column_meta = {}
    filter_column_meta['column_name'] = 'updated_date' if updated_after is not None else 'created_date'
    filter_column_meta['column_condition'] = 'updated_date__gte' if updated_after is not None else 'created_date__gte'


    # when no timezone is provided by the user default to the server default timezone 
    if timezone.is_naive(filter_date):
        filter_date = timezone.make_aware(filter_date)
        
    return True, filter_date, filter_column_meta

def serialize_model_data(data, request):
    if not isinstance(data, QuerySet):
        raise ValueError(f"Expected a QuerySet, got {type(data).__name__}")

    paginator = ApiPagination()
    results_page = paginator.paginate_queryset(data, request)

    if data.model is Purchase:
        serializer = PurchaseSerializer(results_page, many=True)
    elif data.model is PurchaseItem:
        serializer = PurchaseItemSerializer(results_page, many=True)
    elif data.model is Product:
        serializer = ProductSerializer(results_page, many=True)
    else:
        raise ValueError(f'Model instance with no defined serialized passed: {data.model._meta.model_name }')

    # get only the response data instead of the entire Response object
    paginated_data = paginator.get_paginated_response(serializer.data).data
    return paginated_data
