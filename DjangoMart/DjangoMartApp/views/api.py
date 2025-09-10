from ..models import (Product, ShoppingCart, CartItem, 
                     DeliveryDestination, Purchase, PurchaseItem)
from .utility import  (product_has_enough_stock, add_product_to_cart,
                       validate_api_date_parameters, serialize_model_data)

from .serializers import CustomTokenObtainPairSerializer

from django.forms.models import model_to_dict
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchases(request):
    success, response, filter_column_meta = validate_api_date_parameters(request.GET.get('created_after'), request.GET.get('updated_after'))

    if not success:
        return response
    filter_date = response

    purchases = Purchase.objects.filter(
        **{filter_column_meta['column_condition']: filter_date}
        ).order_by(filter_column_meta['column_name'])
    
    purchases_data = serialize_model_data(purchases, request)

    return Response(
    {
        "success": True,
        "data": purchases_data
    },
    status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchase_items(request):
    success, response, filter_column_meta = validate_api_date_parameters(request.GET.get('created_after'), request.GET.get('updated_after'))

    if not success:
        return response
    filter_date = response

    purchase_items = PurchaseItem.objects.filter(
        **{filter_column_meta['column_condition']: filter_date}
        ).order_by(filter_column_meta['column_name'])
    
    purchase_items_data = serialize_model_data(purchase_items, request)

    return Response(
    {
        "success": True,
        "data": purchase_items_data
    },
    status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    success, response, filter_column_meta = validate_api_date_parameters(request.GET.get('created_after'), request.GET.get('updated_after'))

    if not success:
        return response
    filter_date = response

    products = Product.objects.filter(
        **{filter_column_meta['column_condition']: filter_date}
        ).order_by(filter_column_meta['column_name'])
    
    products_data = serialize_model_data(products, request)

    return Response(
    {
        "success": True,
        "data": products_data
    },
    status=status.HTTP_200_OK)