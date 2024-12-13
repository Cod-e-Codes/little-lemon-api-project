"""
URL configuration for LittleLemon project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/', include('LittleLemonAPI.urls')),  # Include app-specific routes
    path('auth/', include('djoser.urls')),  # User authentication routes
    path('auth/', include('djoser.urls.authtoken')),  # Token-based authentication
]
