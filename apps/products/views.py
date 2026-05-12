from rest_framework import viewsets, permissions
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer
from apps.users.permissions import IsStaffUser

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [permissions.AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        # Filter by category if provided in query params
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        # Staff can see inactive products
        if self.request.user.is_authenticated and self.request.user.role in ['STAFF', 'ADMIN']:
            return queryset
        return queryset.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [permissions.AllowAny()]
