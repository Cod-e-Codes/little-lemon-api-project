from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import (
    MenuItemSerializer, 
    CategorySerializer, 
    CartSerializer, 
    OrderSerializer, 
    OrderItemSerializer,
    UserSerializer
)
from .permissions import IsManagerUser, IsDeliveryCrew, IsCustomerUser

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManagerUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        
        # Filtering
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Sorting
        sort_by = self.request.query_params.get('sort')
        if sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == '-price':
            queryset = queryset.order_by('-price')
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(category__title__icontains=search)
            )
        
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManagerUser]

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsCustomerUser]
    
    def list(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        menuitem_id = serializer.validated_data['menuitem_id']
        quantity = serializer.validated_data['quantity']
        menuitem = get_object_or_404(MenuItem, pk=menuitem_id)
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, 
            menuitem=menuitem,
            defaults={
                'quantity': quantity,
                'unit_price': menuitem.price,
                'price': menuitem.price * quantity
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.price = menuitem.price * cart_item.quantity
            cart_item.save()
        
        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsCustomerUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsManagerUser | IsDeliveryCrew]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsManagerUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    
    def create(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total = sum(item.price for item in cart_items)
        
        order = Order.objects.create(
            user=request.user, 
            total=total, 
            status=0
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order, 
                menuitem=cart_item.menuitem, 
                quantity=cart_item.quantity,
                price=cart_item.price
            )
        
        cart_items.delete()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsDeliveryCrew])
    def deliver(self, request, pk=None):
        order = self.get_object()
        order.status = 1  # Mark as delivered
        order.save()
        return Response({"status": "Order delivered"}, status=status.HTTP_200_OK)

class UserGroupManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManagerUser]
    
    @action(detail=False, methods=['GET', 'POST'], url_path='manager/users')
    def manager_users(self, request):
        if request.method == 'GET':
            manager_group = Group.objects.get(name='Manager')
            users = manager_group.user_set.all()
            return Response(UserSerializer(users, many=True).data)
        
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        user.groups.add(manager_group)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET', 'POST'], url_path='delivery-crew/users')
    def delivery_crew_users(self, request):
        if request.method == 'GET':
            delivery_group = Group.objects.get(name='Delivery Crew')
            users = delivery_group.user_set.all()
            return Response(UserSerializer(users, many=True).data)
        
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        delivery_group, _ = Group.objects.get_or_create(name='Delivery Crew')
        user.groups.add(delivery_group)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['DELETE'], url_path='manager/users')
    def remove_from_manager_group(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        manager_group = Group.objects.get(name='Manager')
        user.groups.remove(manager_group)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['DELETE'], url_path='delivery-crew/users')
    def remove_from_delivery_crew(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        delivery_group = Group.objects.get(name='Delivery Crew')
        user.groups.remove(delivery_group)
        return Response(status=status.HTTP_200_OK)