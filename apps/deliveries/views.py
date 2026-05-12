from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Address, Delivery
from .serializers import AddressSerializer, DeliverySerializer
from apps.users.permissions import IsStaffUser

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['STAFF', 'ADMIN']:
            return Delivery.objects.all()
        return Delivery.objects.filter(order__user=user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'assign_driver']:
            return [IsStaffUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def assign_driver(self, request, pk=None):
        delivery = self.get_object()
        driver_id = request.data.get('driver_id')
        if driver_id:
            delivery.driver_id = driver_id
            delivery.status = Delivery.Status.ASSIGNED
            delivery.save()
            return Response(self.get_serializer(delivery).data)
        return Response(
            {"error": "driver_id is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        new_status = request.data.get('status')
        if new_status in Delivery.Status.values:
            delivery.status = new_status
            delivery.save()
            return Response(self.get_serializer(delivery).data)
        return Response(
            {"error": "Invalid status"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
