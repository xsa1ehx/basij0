from pydantic import BaseModel, Field
from typing import Optional

class UserOut(BaseModel):
    id: int
    student_number: str
    role_id: int
    is_active: bool
    profile: Optional[dict] = None

    model_config = {"from_attributes": True}

# Schema برای بروزرسانی پروفایل کاربر
class ProfileUpdate(BaseModel):
    phone_number: Optional[str] = Field(None, pattern=r"^\d{11}$")
    address: Optional[str] = Field(None, max_length=200)
    gender: Optional[str] = Field(None, pattern="^(brother|sister)$")

    model_config = {
        "json_schema_extra": {
            "example": {
                "phone_number": "09123456789",
                "address": "کرمان، بلوار هوانیوز",
                "gender": "brother"
            }
        }
    }