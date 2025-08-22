from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
from dotenv import load_dotenv
from controller import user_controller
from database import get_collection
load_dotenv()
from fastapi.staticfiles import StaticFiles

app = FastAPI()
from routes import user,user_chat

# Configure Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")
app.include_router(user.router)

app.include_router(user_chat.router)
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
# Set up Jinja2 template rendering
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# @app.get("/query/")
# async def query_rag(query: str):
#     retrieved_docs = retrieve_relevant_docs(query)
#     context = "\n".join(retrieved_docs)

#     prompt = f"Use the following context to answer the question:\n{context}\n\nQ: {query}\nA:"
    
#     response = model.generate_content(prompt)

#     return {"response": response.text.strip()}
@app.get("/data")
async def getData():
    collection=get_collection("User")
    data=collection.find({})
    return {"success":True,"data":data,"status_code":200}  

