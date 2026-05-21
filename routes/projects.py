from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from Database.db_connect import collection_projects
from bson import ObjectId

router = APIRouter()


class ProjectModel(BaseModel):
    title: str
    description: str
    project_overview: Optional[str] = ""
    tech_stack: List[str]
    image_urls: List[str] = []
    github_url: Optional[str] = ""
    demo_url: Optional[str] = ""
    is_featured: bool = False


# เรียกดูโปรเจคทั้งหมด
@router.get("/")
def get_projects():
    projects = []
    for doc in collection_projects.find():
        doc["id"] = str(doc.pop("_id"))
        projects.append(doc)
    return {"data": projects, "projects": projects}


# เรียกดูโปรเจคตาม ID
@router.get("/{project_id}")
def get_project_by_id(project_id: str):
    try:
        obj_id = ObjectId(project_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    project = collection_projects.find_one({"_id": obj_id})

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project["id"] = str(project.pop("_id"))

    return {"data": project}


# เพิ่มโปรเจคใหม่
@router.post("/")
def create_project(project: ProjectModel):
    new_project = project.model_dump()

    result = collection_projects.insert_one(new_project)
    return {"message": "Project created successfully", "id": str(result.inserted_id)}


# แก้ไขโปรเจค
@router.put("/{project_id}")
def update_project(project_id: str, project: ProjectModel):
    try:
        obj_id = ObjectId(project_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    update_data = {"$set": project.model_dump()}
    result = collection_projects.update_one({"_id": obj_id}, update_data)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project updated successfully"}


# ลบโปรเจค
@router.delete("/{project_id}")
def delete_project(project_id: str):
    try:
        obj_id = ObjectId(project_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    result = collection_projects.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted successfully"}
