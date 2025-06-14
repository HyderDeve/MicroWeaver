from pydantic import BaseModel

class ProjectPrompt(BaseModel):
    prompt: str
    project_name: str | None = "microservice"

class ProjectResponse(BaseModel):
    message: str
    project_path: str | None = None