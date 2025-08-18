from ..models import (Product, ShoppingCart, CartItem, 
                     DeliveryDestination)
from ..functions import  product_has_enough_stock, add_product_to_cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json 


@login_required
@require_http_methods(['PUT'])
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
@require_http_methods(['PUT'])
def remove_from_cart(request):
    try:
        request_body = json.loads(request.body)
        item_id = request_body.get('cart_item_id')
        
        if not item_id:
            return JsonResponse({'error': 'Item id not provided'}, status=400)
        
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
@require_http_methods(['PUT'])
def add_address(request):

    if request.user.delivery_details_provided_count == 3:
        return JsonResponse({'error': 'You cannot have more than 3 addresses saved'}, status=400)
    
    request_body = json.loads(request.body)
    city = request_body.get('city')
    street = request_body.get('street')
    street_number = request_body.get('street_number')
    phone_number = request_body.get('phone_number')

    if not city or not street or not street_number or not phone_number:
        return JsonResponse({'error': 'Mandatory field not provided'}, status=400)
    
    delivery_destination = DeliveryDestination.objects.create(
        user=request.user,
        city=city,
        street=street,
        street_number=street_number,
        phone_number=phone_number
    )

    request.user.delivery_details_provided_count += 1
    request.user.save()

    return JsonResponse(model_to_dict(delivery_destination, fields=['id']), status=200)

@login_required
@require_http_methods(['PUT'])
def remove_address(request):
    request_body = json.loads(request.body)
    address_id = request_body.get('address_id')
    try:
        delivery_destination = DeliveryDestination.objects.get(
        user=request.user,
        id=address_id
    )
    except DeliveryDestination.DoesNotExist:
        return JsonResponse({'error': 'No such delivery address exists for this user'}, status=404)
    
    delivery_destination.delete()
    request.user.delivery_details_provided_count -= 1
    request.user.save()

    return JsonResponse({'message': 'Address deleted successfully'}, status=200)