from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import BasePermission
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)


# Custom Permissions
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()


# Categories View
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Throttle for both users and anonymous


# Menu Items View
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Throttle for authenticated users
    ordering_fields = ['price', 'title']  # Ordering options
    search_fields = ['title', 'category__title']  # Searching options

    def get_queryset(self):
        # Admins see all menu items, others see only those marked as featured
        if self.request.user.is_staff:
            return MenuItem.objects.all()
        return MenuItem.objects.filter(featured=True)


# Cart View
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Throttle for authenticated users

    def get_queryset(self):
        # Filter carts to show only the current user's items
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user for new cart items
        serializer.save(user=self.request.user)


# Orders View
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Throttle for authenticated users

    def get_queryset(self):
        # Filter orders to show only the current user's orders
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user and calculate total for the new order
        cart_items = Cart.objects.filter(user=self.request.user)
        total = sum(item.total_price for item in cart_items)
        order = serializer.save(user=self.request.user, total=total)
        # Move items from cart to OrderItem
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
            )
        # Clear the cart after order creation
        cart_items.delete()


# Delivery Crew Orders View
class DeliveryOrdersView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsDeliveryCrew]
    throttle_classes = [UserRateThrottle]  # Throttle for authenticated users

    def perform_update(self, serializer):
        # Allow delivery crew to update the order status to "delivered"
        if 'status' in self.request.data:
            serializer.save(status=True)  # Mark as delivered


# Admin Menu Item Management
class AdminMenuItemManagementView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]  # Restrict access to admin users only
    throttle_classes = [UserRateThrottle]
