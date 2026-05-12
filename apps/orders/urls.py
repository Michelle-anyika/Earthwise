from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CartViewSet, CartItemViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'cart/items', CartItemViewSet, basename='cart-item')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
