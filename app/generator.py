import os
import asyncio
from typing import Dict, List, Optional, Any
from enum import Enum
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MicroserviceComponent(Enum):
    MAIN = "MAIN"
    ROUTES = "ROUTES"
    MODELS = "MODELS"
    SCHEMAS = "SCHEMAS"
    SERVICES = "SERVICES"
    CONFIG = "CONFIG"

class CodeGenerator:
    def __init__(self):
        """Initialize the Gemini AI code generator"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini AI
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 8192,
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )

    async def generate_code(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate code based on the provided prompt and context
        
        Args:
            prompt: The user's request for code generation
            context: Additional context information
            
        Returns:
            Generated code as a string
        """
        try:
            # Build the complete prompt
            system_prompt = self._build_system_prompt()
            full_prompt = self._build_code_prompt(prompt, context)
            
            # Generate code using Gemini
            response = await self._generate_with_retry(system_prompt + "\n\n" + full_prompt)
            
            # Clean and return the generated code
            return self._clean_generated_code(response)
            
        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            raise ValueError(f"Failed to generate code: {str(e)}")

    # ============================================================================
    # MAIN MICROSERVICE GENERATION METHOD - HIGHLIGHTED
    # ============================================================================
    async def generate_microservice_code(
        self, 
        prompt: str, 
        components: Optional[List[MicroserviceComponent]] = None
    ) -> Dict[str, str]:
        """
        🎯 CORE METHOD: Generate a complete microservice or specific components
        
        This is the main method that orchestrates the generation of entire
        microservices with multiple components (routes, models, schemas, etc.)
        
        Args:
            prompt: The user's request for microservice generation
            components: List of specific components to generate
            
        Returns:
            Dictionary with component names as keys and generated code as values
        """
        try:
            # If no components specified, generate all
            if not components:
                components = list(MicroserviceComponent)
            
            generated_files = {}
            
            # Generate each component
            for component in components:
                component_code = await self._generate_component(prompt, component)
                generated_files[component.value.lower()] = component_code
            
            return generated_files
            
        except Exception as e:
            logger.error(f"Microservice generation failed: {str(e)}")
            raise ValueError(f"Failed to generate microservice: {str(e)}")
    # ============================================================================

    def _build_system_prompt(self) -> str:
        """Build the system prompt for code generation"""
        return """You are an expert Python developer specializing in FastAPI microservices.
Your task is to generate clean, production-ready code that follows best practices.

Guidelines:
- Use FastAPI framework for API development
- Follow PEP 8 style guidelines
- Include proper error handling
- Add type hints where appropriate
- Include docstrings for functions and classes
- Use Pydantic models for data validation
- Implement proper logging
- Follow RESTful API conventions
- Include necessary imports
- Generate complete, working code

Always return only the code without additional explanations or markdown formatting."""

    def _build_code_prompt(self, prompt: str, context: Optional[Dict[str, Any]]) -> str:
        """Build the complete prompt for code generation"""
        base_prompt = f"Generate Python code based on this request: {prompt}"
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            base_prompt += f"\n\nAdditional context:\n{context_str}"
        
        return base_prompt

    async def _generate_component(self, prompt: str, component: MicroserviceComponent) -> str:
        """Generate code for a specific microservice component"""
        component_prompts = {
            MicroserviceComponent.MAIN: self._get_main_prompt(prompt),
            MicroserviceComponent.ROUTES: self._get_routes_prompt(prompt),
            MicroserviceComponent.MODELS: self._get_models_prompt(prompt),
            MicroserviceComponent.SCHEMAS: self._get_schemas_prompt(prompt),
            MicroserviceComponent.SERVICES: self._get_services_prompt(prompt),
            MicroserviceComponent.CONFIG: self._get_config_prompt(prompt),
        }
        
        system_prompt = self._build_system_prompt()
        component_prompt = component_prompts[component]
        
        response = await self._generate_with_retry(system_prompt + "\n\n" + component_prompt)
        return self._clean_generated_code(response)

    def _get_main_prompt(self, prompt: str) -> str:
        """Generate prompt for main.py file"""
        return f"""Generate a FastAPI main.py file for: {prompt}

The file should include:
- FastAPI app initialization
- Router inclusion
- Basic middleware setup
- Health check endpoint
- Proper CORS configuration if needed
- Error handlers"""

    def _get_routes_prompt(self, prompt: str) -> str:
        """Generate prompt for routes"""
        return f"""Generate FastAPI router code for: {prompt}

The routes should include:
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Request/response models
- Error handling
- Input validation
- Appropriate status codes
- Route documentation"""

    def _get_models_prompt(self, prompt: str) -> str:
        """Generate prompt for database models"""
        return f"""Generate database models for: {prompt}

The models should include:
- SQLAlchemy or similar ORM models
- Proper relationships
- Table definitions
- Indexes where appropriate
- Model methods if needed"""

    def _get_schemas_prompt(self, prompt: str) -> str:
        """Generate prompt for Pydantic schemas"""
        return f"""Generate Pydantic schemas for: {prompt}

The schemas should include:
- Request/response models
- Data validation
- Field descriptions
- Optional/required fields
- Type hints
- Serialization methods if needed"""

    def _get_services_prompt(self, prompt: str) -> str:
        """Generate prompt for service layer"""
        return f"""Generate service layer code for: {prompt}

The services should include:
- Business logic separation
- Database operations
- Error handling
- Logging
- Async/await patterns
- Data processing methods"""

    def _get_config_prompt(self, prompt: str) -> str:
        """Generate prompt for configuration"""
        return f"""Generate configuration code for: {prompt}

The configuration should include:
- Environment variables handling
- Settings management
- Database configuration
- API keys management
- Logging configuration
- Development/production settings"""

    async def _generate_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Generate code with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                
                if response.candidates and response.candidates[0].content:
                    return response.candidates[0].content.parts[0].text
                else:
                    raise ValueError("No content generated")
                    
            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(1)  # Brief delay before retry
        
        raise ValueError("Failed to generate content after retries")

    def _clean_generated_code(self, code: str) -> str:
        """Clean and format the generated code"""
        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        
        if code.endswith("```"):
            code = code[:-3]
        
        # Remove leading/trailing whitespace
        code = code.strip()
        
        # Ensure proper line endings
        code = code.replace('\r\n', '\n')
        
        return code

# Global instance
code_generator = CodeGenerator()