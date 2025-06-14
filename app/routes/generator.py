# route/genrator.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.project import ProjectPrompt, ProjectResponse
from app.utils.generator import ProjectGenerator
import tempfile
import os
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.generator import code_generator
from app.schemas.generator import (
    GenerateCodeRequest,
    GenerateCodeResponse,
    GenerateMicroserviceRequest,
    GenerateMicroserviceResponse
)
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
                                'readme_md': f"""# Generated Microservice

                This microservice was generated based on the prompt: {prompt.prompt}

                ## Running the application

                ```bash
                uvicorn app.main:app --reload
                """
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CodeGenerationRequest(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = None

class CodeGenerationResponse(BaseModel):
    generated_code: str

@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code using Gemini AI based on the provided prompt and context."""
    try:
        generated_code = await code_generator.generate_code(
            prompt=request.prompt,
            context=request.context
        )
        return CodeGenerationResponse(generated_code=generated_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code generation failed: {str(e)}"
        )


@router.post("/generate/microservice", response_model=GenerateMicroserviceResponse)
async def generate_microservice(request: GenerateMicroserviceRequest):
    """Generate a complete microservice or specific components based on the prompt."""
    try:
        # Convert schema ComponentType to generator MicroserviceComponent
        components = None
        if request.components:
            components = [
                getattr(MicroserviceComponent, comp.value.upper())
                for comp in request.components
            ]
        
        generated_code = await code_generator.generate_microservice_code(
            prompt=request.prompt,
            components=components
        )
        return GenerateMicroserviceResponse(generated_code=generated_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Microservice generation failed: {str(e)}"
        )