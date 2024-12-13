from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    # Menu Items
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.AdminMenuItemManagementView.as_view(), name='menu-item-detail'),

    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),

    # Orders
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('delivery-orders/', views.DeliveryOrdersView.as_view(), name='delivery-orders'),

    # Groups
    path('groups/<str:group_name>/users/', views.ManageGroupUsersView.as_view(), name='manage-group-users'),

]
