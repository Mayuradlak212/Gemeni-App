from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    phone: str = Field(..., min_length=10, max_length=15)
    password: str  # Hashed password
    otp: Optional[int] = None
    token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    lastLogin: List[datetime] = []
    status: bool = Field(default=False)  # ✅ Corrected
