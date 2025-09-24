from .utility import  get_standart_api_model_data

from .serializers import CustomTokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchases(request):
    return get_standart_api_model_data(request, 'Purchase')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchase_items(request):
    return get_standart_api_model_data(request, 'PurchaseItem')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    return get_standart_api_model_data(request, 'Product')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    return get_standart_api_model_data(request, 'User')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    return get_standart_api_model_data(request, 'Category')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews(request):
    return get_standart_api_model_data(request, 'Review')