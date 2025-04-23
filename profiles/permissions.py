from rest_framework.permissions import BasePermission


class IsPremiumUser(BasePermission):
    """
    Custom permission to only allow access to premium users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_premium
