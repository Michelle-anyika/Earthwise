from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer
from apps.users.permissions import IsStaffUser

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        queryset = Inventory.objects.all()
        source_type = self.request.query_params.get('source_type', None)
        if source_type:
            queryset = queryset.filter(source_type=source_type)
        return queryset

    @action(detail=False, methods=['get'])
    def low_stock_alerts(self, request):
        low_stock_items = [
            item for item in Inventory.objects.all() if item.is_low_stock
        ]
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        inventory = self.get_object()
        quantity = request.data.get('quantity', 0)
        action_type = request.data.get('action', 'add') # add or subtract

        try:
            quantity = float(quantity)
            if action_type == 'add':
                inventory.quantity_kg += quantity
            elif action_type == 'subtract':
                inventory.quantity_kg -= quantity
            
            inventory.save()
            return Response(self.get_serializer(inventory).data)
        except ValueError:
            return Response(
                {"error": "Invalid quantity"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
