from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, Cart, CartItem
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer
from apps.users.permissions import IsStaffUser

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role in ['STAFF', 'ADMIN']:
                return Order.objects.all()
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Only staff can update status
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return Response(self.get_serializer(order).data)
        return super().update(request, *args, **kwargs)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        obj, created = Cart.objects.get_or_create(user=self.request.user)
        return obj

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
