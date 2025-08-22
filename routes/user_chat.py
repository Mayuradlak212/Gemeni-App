from fastapi import APIRouter
from controller.user_chat import ask_question,get_user_chats
from models.question import Question

router = APIRouter(prefix="/qa", tags=["users"])

@router.post("/ask", response_model=dict)
async def ask_question_route(data: Question):  # Renamed to avoid recursion
    print("Request is Here ")
    return await ask_question(data)  # ✅ Await the async function
@router.get("/chats/{user_id}", response_model=dict)
async def get_chats_route(user_id: str):
    return await get_user_chats(user_id)