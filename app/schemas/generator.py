from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class ComponentType(str, Enum):
    MAIN = "main"
    ROUTES = "routes"
    MODELS = "models"
    SCHEMAS = "schemas"
    SERVICES = "services"
    CONFIG = "config"

class GenerateCodeRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Description of the code to generate")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for code generation")

class GenerateMicroserviceRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Description of the microservice to generate")
    components: Optional[List[ComponentType]] = Field(
        None,
        description="Specific components to generate. If not provided, all components will be generated"
    )

class GenerateCodeResponse(BaseModel):
    generated_code: str

class GenerateMicroserviceResponse(BaseModel):
    generated_code: Dict[str, str]