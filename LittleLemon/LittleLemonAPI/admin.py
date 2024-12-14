from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

# Custom User Admin to show groups
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_groups',)
    
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')

# MenuItem Admin
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'featured')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'category__title')
    list_editable = ('price', 'featured')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity', 'unit_price', 'price')
    list_filter = ('user', 'menuitem__category')
    search_fields = ('user__username', 'menuitem__title')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'menuitem')

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'date', 'delivery_crew')
    list_filter = ('status', 'date', 'delivery_crew')
    search_fields = ('user__username', 'id')
    list_editable = ('status', 'delivery_crew')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'delivery_crew')

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'price')
    list_filter = ('order__user', 'menuitem__category')
    search_fields = ('order__id', 'menuitem__title')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'menuitem')

# Replace default User admin with custom User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)