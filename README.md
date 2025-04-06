# CapstoneProject
 This project is an Inventory Management API using Django and Django REST Framework (DRF). This API will enable users to manage inventory items by adding, updating, deleting, and viewing inventory levels. The API will support user authentication and inventory tracking, simulating a real-world inventory management system for a store.

REGISTRATION AND LOGGING IN
 Register a User:
    URL: http://127.0.0.1:8000/api/register/
    Method: POST
    Headers:
        Content-Type: application/json
    Body (raw → JSON):
    {
  "username": "branice",
  "password": "StrongPassword123",
  "email": "branice@example.com"
    }
    Expected Response when you successfully log in:
{
  "message": "User registered successfully"
}

LOGIN AS A USER:
You have two options:
Option A: Your custom login endpoint
    URL: http://127.0.0.1:8000/api/token/
    Method: POST
    Headers:
        Content-Type: application/json
    Body:
{
  "username": "branice",
  "password": "StrongPassword123"
}
    Expected Response:
{
  "refresh": "your-refresh-token",
  "access": "your-access-token"
}

Option B: Default JWT token obtain pair view from SimpleJWT
    URL: http://127.0.0.1:8000/api/token/
    Method: POST
    Body:
{
  "username": "branice",
  "password": "StrongPassword123"
}
    Expected Response: Is the same as Option A.

Refresh Access Token this is when you access token expires...
    URL: http://127.0.0.1:8000/api/token/refresh/
    Method: POST
    Headers:
        Content-Type: application/json
    Body:
{
  "refresh": "your-refresh-token"
}
    Expected Response:
{
  "access": "new-access-token"
}






THIS IS AN EXAMPLE OF HOW TO PERFORM CRUD OPERATIONS
Create Inventory Item (POST)
    URL: http://localhost:8000/api/inventory/create/
    Method: POST
    Headers:
        Authorization: Bearer <your_token> (Use JWT token here for authentication)
        Content-Type: application/json
        {
        "name": "New Item",
        "description": "This is a new inventory item",
        "quantity": 50,
        "price": 20.99,
        "category": "Electronics"
        }

Get All Inventory Items (GET)
    URL: http://localhost:8000/api/inventory/
    Method: GET
    Headers:
        Authorization: Bearer <your_token>
    Response:


Update Inventory Item (PUT)
    URL: http://localhost:8000/api/inventory/<id>/update/ 
    Method: PUT
    Headers:
        Authorization: Bearer <your_token>
        Content-Type: application/json
    Body (JSON):
    Update Inventory Item (PUT)
    {
    "name": "Updated Item",
    "description": "Updated description of the inventory item",
    "quantity": 100,
    "price": 25.50,
    "category": "Electronics"
    }


Delete Inventory Item (DELETE)
    URL: http://localhost:8000/api/inventory/<id>/delete/ 
    Method: DELETE
    Headers:
        Authorization: Bearer <your_token>
    Response:
    {
    "status": "success",
    "message": "Item deleted successfully"
    }