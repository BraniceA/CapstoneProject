from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions  # Import necessary components from DRF
from rest_framework.decorators import api_view, permission_classes  # Import decorators for API views and permissions
from rest_framework.response import Response  # Import Response to return API responses
from .models import InventoryItem  # Import the InventoryItem model
from .serializers import InventoryItemSerializer  # Import the InventoryItemSerializer

# Create Inventory Item
@api_view(['POST'])  # Define this view to respond to POST requests
@permission_classes([permissions.IsAuthenticated])  # Ensure only authenticated users can access this view
def create_inventory_item(request):  # Define the function to create an inventory item
    if request.method == 'POST':  # Check if the request method is POST
        serializer = InventoryItemSerializer(data=request.data)  # Initialize the serializer with the data from the request
        if serializer.is_valid():  # Check if the data is valid
            serializer.save(user=request.user)  # Save the item and associate it with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created item with a success status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors if any

# Get all Inventory Items
@api_view(['GET'])  # Define this view to respond to GET requests
@permission_classes([permissions.IsAuthenticated])  # Ensure only authenticated users can access this view
def get_inventory_items(request):  # Define the function to retrieve inventory items
    if request.method == 'GET':  # Check if the request method is GET
        items = InventoryItem.objects.filter(user=request.user)  # Get items belonging to the logged-in user
        serializer = InventoryItemSerializer(items, many=True)  # Serialize the list of items
        return Response(serializer.data)  # Return the serialized data as the response

# Update an Inventory Item
@api_view(['PUT'])  # Define this view to respond to PUT requests
@permission_classes([permissions.IsAuthenticated])  # Ensure only authenticated users can access this view
def update_inventory_item(request, pk):  # Define the function to update an inventory item by primary key
    try:
        item = InventoryItem.objects.get(pk=pk, user=request.user)  # Try to get the item, ensuring it's the logged-in user's item
    except InventoryItem.DoesNotExist:  # If the item doesn't exist, catch the error
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)  # Return an error if item not found

    if request.method == 'PUT':  # Check if the request method is PUT
        serializer = InventoryItemSerializer(item, data=request.data)  # Initialize the serializer with existing item data and new request data
        if serializer.is_valid():  # Check if the data is valid
            serializer.save()  # Save the updated item
            return Response(serializer.data)  # Return the updated item as the response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors if any

# Delete an Inventory Item
@api_view(['DELETE'])  # Define this view to respond to DELETE requests
@permission_classes([permissions.IsAuthenticated])  # Ensure only authenticated users can access this view
def delete_inventory_item(request, pk):  # Define the function to delete an inventory item by primary key
    try:
        item = InventoryItem.objects.get(pk=pk, user=request.user)  # Try to get the item, ensuring it's the logged-in user's item
    except InventoryItem.DoesNotExist:  # If the item doesn't exist, catch the error
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)  # Return an error if item not found

    if request.method == 'DELETE':  # Check if the request method is DELETE
        item.delete()  # Delete the item from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return a success status with no content



# views.py

from rest_framework_simplejwt.tokens import RefreshToken  # Import RefreshToken to generate JWT
from rest_framework.views import APIView  # Import APIView to create a custom view
from rest_framework.response import Response  # Import Response to send HTTP responses
from rest_framework import status  # Import status for HTTP status codes
from django.contrib.auth.models import User  # Import User model to validate credentials

class ObtainTokenView(APIView):  # Define the view to handle JWT token generation
    def post(self, request):  # Define POST method to handle the request for token generation
        username = request.data.get('username')  # Get the username from the request data
        password = request.data.get('password')  # Get the password from the request data

        user = User.objects.filter(username=username).first()  # Find the user by username
        if user and user.check_password(password):  # Check if user exists and if password matches
            refresh = RefreshToken.for_user(user)  # Create a RefreshToken for the authenticated user
            access_token = str(refresh.access_token)  # Get the access token from the refresh token
            return Response({'access': access_token}, status=status.HTTP_200_OK)  # Return the token in response
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)  # Return error for invalid credentials


# inventory/views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import AllowAny

# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Registration view
class RegisterUser(APIView):
    permission_classes = [AllowAny]  #Allow anyone to access this endpoint
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login view (using JWT authentication)
class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
