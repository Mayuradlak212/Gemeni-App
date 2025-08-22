from fastapi import APIRouter, HTTPException
from datetime import datetime
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

from models.question import Question  # Import Pydantic model
from dotenv import load_dotenv
import os
from database import get_collection
# Load environment variables from .env file
load_dotenv()
qa_collection = get_collection("question")
# Get MongoDB URI and database name from environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

print("KEY ", API_KEY)
router = APIRouter()

# Load Embedding Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load Google Gemini API
genai.configure(api_key=API_KEY)

def get_embedding(text):
    return embedding_model.encode(text).tolist()

def generate_response(question):
    """Generate response using Gemini API"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Corrected
        response = model.generate_content(question)  # ✅ Corrected
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        return "Error generating response."
 

async def ask_question(data: Question):
    try:
        # Step 1: Store question with embedding
        print("data ",data)
        embedding = get_embedding(data.question)
        question_data = {
            "user_id": data.user_id,
            "question": data.question,
            "embedding": embedding,
            "response": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        inserted_doc = qa_collection.insert_one(question_data)

        # Step 2: Generate response & update document
        response = generate_response(data.question)
        qa_collection.update_one(
            {"_id": inserted_doc.inserted_id},
            {"$set": {"response": response, "updated_at": datetime.utcnow()}}
        )

        return {"query_id": str(inserted_doc.inserted_id), "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_user_chats(user_id: str):
    try:
        chats = list(qa_collection.find({"user_id": user_id}, {"_id":0,"embedding": 0}))  # Exclude _id
        if not chats:
            return {"success": False, "message": "No chats found for this user.", "data": []}

        return {"success": True, "message": "Chats retrieved successfully.", "data": chats}

    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": str(e), "data": []})