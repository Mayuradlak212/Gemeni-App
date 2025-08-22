from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Question(BaseModel):
    user_id: str
    question: str
    embedding: list
    response: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
