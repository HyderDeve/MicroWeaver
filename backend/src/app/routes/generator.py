from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.project import ProjectPrompt, ProjectResponse
from app.utils.generator import ProjectGenerator
import tempfile
import os

router = APIRouter()

@router.post("/generate", response_model=ProjectResponse)
async def generate_project(prompt: ProjectPrompt):
    try:
        # Create a temporary directory for the project
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = os.path.join(temp_dir, prompt.project_name)
            
            # Initialize project generator
            generator = ProjectGenerator(project_path)
            
            # Create basic structure
            await generator.create_directory_structure()
            
            # Define template data (you can make this dynamic based on the prompt)
            template_data = {
                'main_py': '''from fastapi import FastAPI
from app.routes import users

app = FastAPI()
app.include_router(users.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the generated microservice"}
''',
                'requirements_txt': '''fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
''',
                'dockerfile': '''FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',
                'readme_md': f'''# Generated Microservice

This microservice was generated based on the prompt: {prompt.prompt}

## Running the application

```bash
uvicorn app.main:app --reload
"""
            }