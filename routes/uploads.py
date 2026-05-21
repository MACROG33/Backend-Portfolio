from fastapi import APIRouter, HTTPException, UploadFile, File
import cloudinary.uploader
from Database.db_connect import cloudinary

router = APIRouter()


@router.post("/")
def upload_file(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, folder="portfolio_assets")

        return {"url": result.get("secure_url"), "public_id": result.get("public_id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
