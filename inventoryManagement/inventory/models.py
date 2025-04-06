from django.db import models                     # Import base model functionality
from django.contrib.auth.models import User       # Import built-in Django User model
from django.utils import timezone                # Import timezone utilities for timestamps
from django.conf import settings                 # Import Django settings for configuration
# Create your models here.

# InventoryItem model: represents an item in the inventory
class InventoryItem(models.Model):
    name = models.CharField(max_length=255)       # Required: Name of the item
    description = models.TextField(blank=True)    # Optional: Description of the item
    quantity = models.PositiveIntegerField()      # Required: Quantity must be >= 0
    price = models.DecimalField(                  # Required: Price of the item
        max_digits=10,                            # Total digits allowed (e.g., 99999999.99)
        decimal_places=2                          # Digits after decimal point
    )
    category = models.CharField(                  # Optional: Category of item
        max_length=100,
        blank=True
    )
    date_added = models.DateTimeField(            # Auto set when item is first created
        auto_now_add=True
    )
    last_updated = models.DateTimeField(          # Auto update every time the item is saved
        auto_now=True
    )
    user = models.ForeignKey(                     # Foreign key to the user who owns this item
        User,
        on_delete=models.CASCADE,                 # Delete items if user is deleted
        related_name='inventory_items'            # Allows reverse lookup from user
    )

    def __str__(self):
        return self.name                          # Display item name in admin or console

    # Validation checks
    def clean(self):  # Custom validation method to ensure certain conditions are met
        if not self.name:  # Check if the name field is empty
            raise ValueError("Item name is required")  # Raise an error if the name is empty
        if self.quantity < 0:  # Check if the quantity is less than 0
            raise ValueError("Quantity cannot be negative")  # Raise an error if the quantity is negative
        if self.price <= 0:  # Check if the price is less than or equal to 0
            raise ValueError("Price must be greater than zero")  # Raise an error if the price is zero or negative



# InventoryChangeLog model: tracks quantity changes for each item (e.g., restocks or sales)
class InventoryChangeLog(models.Model):
    CHANGE_TYPES = (                              # Dropdown options for type of change
        ('restock', 'Restocked'),                 # When items are added
        ('sale', 'Sold'),                         # When items are sold
    )

    item = models.ForeignKey(                     # Link to the affected InventoryItem
        InventoryItem,
        on_delete=models.CASCADE,                 # Delete log if item is deleted
        related_name='change_logs'                # Reverse lookup from item
    )
    user = models.ForeignKey(                     # User who made the change
        User,
        on_delete=models.SET_NULL,                # Keep log even if user is deleted
        null=True
    )
    change_type = models.CharField(               # Whether it was a sale or restock
        max_length=10,
        choices=CHANGE_TYPES
    )
    quantity_changed = models.PositiveIntegerField()  # How many items changed
    timestamp = models.DateTimeField(                 # Auto set when the change is logged
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.change_type} - {self.item.name} - {self.quantity_changed}"
