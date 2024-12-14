from rest_framework.permissions import BasePermission

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return not (request.user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists())