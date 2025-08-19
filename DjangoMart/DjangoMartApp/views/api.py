from ..models import (Product, ShoppingCart, CartItem, 
                     DeliveryDestination, Purchase)
from ..functions import  product_has_enough_stock, add_product_to_cart, parse_date
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        if not product_id or not quantity:
            return Response({'error': 'Missing product_id or quantity'}, status=status.HTTP_400_BAD_REQUEST)

        quantity = int(quantity)
        if quantity <= 0:
            return Response({'error': 'Quantity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)
        
        if product_has_enough_stock(product, quantity):
            add_product_to_cart(request.user, product, quantity) 
            return Response({'message': 'Product added successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Requested quantity exceeds our stock'}, status=status.HTTP_409_CONFLICT)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    try:
        item_id = request.data.get('cart_item_id')
        
        if not item_id:
            return Response({'error': 'Item id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = CartItem.objects.get(id=item_id)
        cart = ShoppingCart.objects.get(user_id=request.user)

        if cart_item.cart != cart:
            return Response({'error': 'You can only manipulate your own cart!'}, status=status.HTTP_403_FORBIDDEN)

        cart.total_items_count -= cart_item.quantity
        cart_item.delete()

        cart.save()

        return Response({'message': 'Succesfully removed item from cart'}, status=status.HTTP_200_OK)

    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_address(request):

    if request.user.delivery_details_provided_count >= 3:
        return Response({'error': 'You cannot have more than 3 addresses saved'}, status=status.HTTP_400_BAD_REQUEST)
    
    city = request.data.get('city')
    street = request.data.get('street')
    street_number = request.data.get('street_number')
    phone_number = request.data.get('phone_number')

    if not all([city, street, street_number, phone_number]):
        return Response({'error': 'Mandatory field not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    delivery_destination = DeliveryDestination.objects.create(
        user=request.user,
        city=city,
        street=street,
        street_number=street_number,
        phone_number=phone_number
    )

    request.user.delivery_details_provided_count += 1
    request.user.save()

    return Response(model_to_dict(delivery_destination, fields=['id']), status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_address(request):
    address_id = request.data.get('address_id')
    try:
        delivery_destination = DeliveryDestination.objects.get(
        user=request.user,
        id=address_id
    )
    except DeliveryDestination.DoesNotExist:
        return Response({'error': 'No such delivery address exists for this user'}, status=status.HTTP_404_NOT_FOUND)
    
    delivery_destination.delete()
    request.user.delivery_details_provided_count -= 1
    request.user.save()

    return Response({'message': 'Address deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchases(request):
    updated_after = parse_date(request.GET.get('updated_after'))
    created_after = parse_date(request.GET.get('created_after'))

    if updated_after is not None and created_after is not None:
        return Response(
            {
                'success':False,
                'message': 'Created_after and updated_after cannot be passed at the same time'
            },
            status=status.HTTP_400_BAD_REQUEST)
    elif updated_after is None and created_after is None:
        return Response(
            {
            'success':False,
            'message': 'Supplying updated_after or created_after parameter is required. Passed dates need to be in valid ISO 8601 format'
            }, 
             status=status.HTTP_400_BAD_REQUEST)
    
    filter_date = updated_after if updated_after is not None else created_after
    
    if updated_after is not None:
        products = Product.objects.filter(updated_after__gte=filter_date)
    else:
        products = Product.objects.filter(created_after__gte=filter_date)

    products = list(products.values())

    return Response({"success": True, "products": products}, status=status.HTTP_200_OK)
