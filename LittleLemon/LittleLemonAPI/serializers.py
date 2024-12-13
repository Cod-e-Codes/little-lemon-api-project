from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Include detailed category info
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )  # Accept category_id for POST/PUT

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)  # Include detailed menu item info
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )  # Accept menu_item_id for POST/PUT

    class Meta:
        model = Cart
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'unit_price', 'total_price']


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)  # Include detailed menu item info
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )  # Accept menu_item_id for POST/PUT

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'unit_price', 'total_price']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)  # Nested OrderItems
    delivery_crew = serializers.StringRelatedField()  # Show delivery crew's username
    delivery_crew_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='delivery_crew', write_only=True, allow_null=True
    )  # Accept delivery_crew_id for assignment

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'date', 'delivery_crew', 'delivery_crew_id', 'items']
