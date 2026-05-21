from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from Database.db_connect import collection_skills
from bson import ObjectId


router = APIRouter()


class SkillItem(BaseModel):
    name: str
    icon: str


class SkillModel(BaseModel):
    category: str
    category_image: Optional[str] = ""
    items: List[SkillItem]


# เรียกดูข้อมูลทักษะทั้งหมด
@router.get("/")
def get_skills():
    skills = []
    for doc in collection_skills.find():
        doc["id"] = str(doc.pop("_id"))
        skills.append(doc)
    return {"skills": skills}


# เพิ่มทักษะใหม่
@router.post("/")
def add_skill(skill: SkillModel):
    result = collection_skills.insert_one(skill.model_dump())
    return {"message": "เพิ่มทักษะสำเร็จ!", "inserted_id": str(result.inserted_id)}


# แก้ไขทักษะ
@router.put("/{skill_id}")
def update_skill(skill_id: str, skill: SkillModel):
    try:
        obj_id = ObjectId(skill_id)
        result = collection_skills.update_one(
            {"_id": obj_id}, {"$set": skill.model_dump()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="ไม่พบกลุ่มทักษะนี้")
        return {"message": "แก้ไขทักษะสำเร็จ!"}
    except Exception:
        raise HTTPException(status_code=400, detail="ID ไม่ถูกต้อง")


# ลบทักษะ
@router.delete("/{skill_id}")
def delete_skill(skill_id: str):
    try:
        result = collection_skills.delete_one({"_id": ObjectId(skill_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="ไม่พบกลุ่มทักษะที่จะลบ")
        return {"message": "ลบทักษะสำเร็จ!"}
    except Exception:
        raise HTTPException(status_code=400, detail="ID ไม่ถูกต้อง")
