from fastapi import FastAPI
from routes import profile, projects, skills, uploads
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to my Portfolio API!"}


app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["Uploads"])
