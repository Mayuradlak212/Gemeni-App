from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId
import bcrypt
from database import get_collection

# MongoDB users collection
users_collection = get_collection("users")

# Hash password function
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

# Create User
def create_user(user_data: dict):
    try:
        # Check if email already exists
        existing_user = users_collection.find_one({"email": user_data["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Hash password
        user_data["password"] = hash_password(user_data["password"])
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        user_data["lastLogin"] = []
        user_data["status"] = "active"

        # Insert into database
        user_id = users_collection.insert_one(user_data).inserted_id
        return {"success": True, "message": "User registered successfully", "user_id": str(user_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

# Get User by ID
def get_user(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})  # Exclude password
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return {"success": True, "user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# Get User by Email
def get_user_by_email(email: str):
    try:
        user = users_collection.find_one({"email": email}, {"password": 0})  # Exclude password
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])
        return {"success": True, "user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# Update User
def update_user(user_id: str, user_data: dict):
    try:
        user_data["updated_at"] = datetime.utcnow()

        update_result = users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made")

        return {"success": True, "message": "User updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

# Delete User
def delete_user(user_id: str):
    try:
        delete_result = users_collection.delete_one({"_id": ObjectId(user_id)})

        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"success": True, "message": "User deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
