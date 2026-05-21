from fastapi import APIRouter, HTTPException
from git import Optional
from pydantic import BaseModel
from Database.db_connect import collection_profile


router = APIRouter()


class ProfileModel(BaseModel):
    name: str
    role: str
    bio: str    
    profile_image: Optional[str] = ""
    resume_url: Optional[str] = ""
    github: Optional[str] = ""
    linkedin: Optional[str] = ""
    email: str


# เรียกดูข้อมูลโปรไฟล์
@router.get("/")
def get_profile():
    profile = collection_profile.find_one({}, {"_id": 0})

    if not profile:
        return {"data": None, "message": "ยังไม่มีข้อมูลโปรไฟล์ในระบบ"}

    return {"data": profile}


# แก้ไขข้อมูลโปรไฟล์
@router.put("/")
def update_profile(profile: ProfileModel):
    result = collection_profile.update_one(
        {}, {"$set": profile.model_dump()}, upsert=True
    )

    if result.modified_count == 0 and not result.upserted_id:
        raise HTTPException(status_code=400, detail="Failed to update profile")

    return {"message": "Profile updated successfully"}
