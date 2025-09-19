from ..models import (Product, ShoppingCart, CartItem, 
                     DeliveryDestination, Review, PurchaseItem)
from .utility import  product_has_enough_stock, add_product_to_cart

from .serializers import CustomTokenObtainPairSerializer

from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manage_review(request):
    purchase_item_id = request.data.get('purchase_item_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment')
    
    if not all([purchase_item_id, rating]):
        return Response({'error': 'Mandatory field not provided'}, status=status.HTTP_400_BAD_REQUEST)
    rating = int(rating)

    try:
        purchase_item = PurchaseItem.objects.get(
        id=purchase_item_id
    )
    except PurchaseItem.DoesNotExist:
        return Response({'error': 'No such purchase item exists for this user'}, status=status.HTTP_404_NOT_FOUND)
    
    if purchase_item.purchase.user != request.user:
        return Response({'error': 'You can only rate your own purchase items'}, status=status.HTTP_404_NOT_FOUND)

    try:
        review, created = Review.objects.get_or_create(user=request.user,purchase_item=purchase_item)
        review.rating = rating 
        review.comment = comment
        review.save()
    except ValidationError:
        return Response({'error': 'Invalid value passed for rating'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Product rated succesfully'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request):
    review_id = request.data.get('review_id')

    if not review_id:
        return Response({'error': 'Mandatory field not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        review = Review.objects.get(user=request.user, id=review_id)
    except Review.DoesNotExist:
        return Response({'error': 'Such review does not exist for this user'}, status=status.HTTP_404_BAD_REQUEST)

    review.delete()

    return Response({'message': 'Review deleted succesfully'}, status=status.HTTP_200_OK)