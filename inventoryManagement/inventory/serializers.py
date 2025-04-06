from rest_framework import serializers  # Import Django Rest Framework's serializers module
from .models import InventoryItem  # Import the InventoryItem model from the models.py file
from django.contrib.auth.models import User  # Import the User model for user registration

# Serializer for Inventory Item Model
class InventoryItemSerializer(serializers.ModelSerializer):  # Define the serializer for the InventoryItem model
    class Meta:  # Meta class to define configuration for the serializer
        model = InventoryItem  # Specify the model that this serializer will work with
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category', 'date_added', 'last_updated', 'user']  # Fields to include in the serializer
        read_only_fields = ['user']   #Update your serializer to exclude the user from being required in input, and only include it when reading data

    def validate_quantity(self, value):  # Custom validation for the quantity field
        if value < 0:  # Check if the value is less than 0
            raise serializers.ValidationError("Quantity cannot be negative")  # Raise an error if the quantity is negative
        return value  # Return the value if it's valid

    def validate_price(self, value):  # Custom validation for the price field
        if value <= 0:  # Check if the price is less than or equal to 0
            raise serializers.ValidationError("Price must be greater than zero")  # Raise an error if the price is invalid
        return value  # Return the price if it's valid


