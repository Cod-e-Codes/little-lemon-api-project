from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem


# Customizing the Admin Interface for better usability
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'featured', 'category')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'category__title')
    ordering = ('title',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'menu_item', 'quantity', 'unit_price', 'total_price')
    list_filter = ('user',)
    search_fields = ('user__username', 'menu_item__title')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'date', 'delivery_crew')
    list_filter = ('status', 'delivery_crew')
    search_fields = ('user__username', 'delivery_crew__username')
    ordering = ('-date',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'unit_price', 'total_price')
    list_filter = ('order',)
    search_fields = ('order__id', 'menu_item__title')
