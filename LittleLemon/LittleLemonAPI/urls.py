from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuItemViewSet, 
    CategoryViewSet, 
    CartViewSet, 
    OrderViewSet,
    UserGroupManagementViewSet
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    
    # User Group Management Endpoints
    path('groups/manager/users', 
         UserGroupManagementViewSet.as_view({'get': 'manager_users', 'post': 'manager_users'}), 
         name='manager-users'),
    path('groups/delivery-crew/users', 
         UserGroupManagementViewSet.as_view({'get': 'delivery_crew_users', 'post': 'delivery_crew_users'}), 
         name='delivery-crew-users'),
]