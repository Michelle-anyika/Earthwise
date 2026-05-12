from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Allows access only to Admin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsStaffUser(permissions.BasePermission):
    """Allows access to Staff and Admin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['STAFF', 'ADMIN'])

class IsBusinessCustomer(permissions.BasePermission):
    """Allows access only to Business Customers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'BUSINESS_CUSTOMER')

class IsCustomer(permissions.BasePermission):
    """Allows access only to regular Customers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'CUSTOMER')
