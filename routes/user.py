from fastapi import APIRouter
from controller.user_controller import create_user, get_user, get_user_by_email, update_user, delete_user
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/",response_model=dict)
async def register_user(user: User):
    print("data ",user)
    return create_user(user.dict())

@router.get("/{user_id}",response_model=dict)
async def fetch_user(user_id: str):
    return get_user(user_id)

@router.get("/email/{email}",response_model=dict)
async def fetch_user_by_email(email: str):
    return get_user_by_email(email)

@router.put("/{user_id}",response_model=dict)
async def modify_user(user_id: str, user_data: dict):
    return update_user(user_id, user_data)

@router.delete("/{user_id}" ,response_model=dict)
async def remove_user(user_id: str):
    return delete_user(user_id)
