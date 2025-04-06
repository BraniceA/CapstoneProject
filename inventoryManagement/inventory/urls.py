from django.urls import path, include  # Import path function to define URL routes
from . import views  # Import views from the current directory
from .views import RegisterUser, LoginUser  # Import RegisterUser and LoginUser classes
from rest_framework_simplejwt.views import TokenObtainPairView as ObtainTokenView, TokenRefreshView, TokenObtainPairView  # Import JWT views

urlpatterns = [  # Define the URL patterns for the app
    path('register/', RegisterUser.as_view(), name='register'), # URL to register a new user
    path('login/', LoginUser.as_view(), name='login'), # URL to log in a user
    path('inventory/', views.get_inventory_items, name='get_inventory_items'),  # URL to get all inventory items
    path('inventory/create/', views.create_inventory_item, name='create_inventory_item'),  # URL to create a new inventory item
    path('inventory/<int:pk>/update/', views.update_inventory_item, name='update_inventory_item'),  # URL to update an inventory item
    path('inventory/<int:pk>/delete/', views.delete_inventory_item, name='delete_inventory_item'),  # URL to delete an inventory item
]
