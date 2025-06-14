# MicroWeaver 🧵🚀

**MicroWeaver** is a FastAPI-based full-stack application that generates microservice scaffolds from natural language prompts like:

> "Create a user management microservice with REST APIs"

It dynamically builds the file and folder structure for a complete backend microservice using Gemini AI, perfect for rapid prototyping, hackathons, and dev acceleration.

## ✨ Features

- 🔤 Natural language to code generation using Gemini AI
- 🛠️ Modern FastAPI backend with PostgreSQL integration
- 📊 Database migrations using Alembic
- 🔒 Environment-based configuration
- 📁 Clean modular architecture:
  - `/app/api/routes/` - API endpoints
  - `/app/core/` - Core configurations
  - `/app/models/` - Database models
  - `/app/services/` - Business logic
  - `/app/schemas/` - Pydantic models
  - `/app/generator.py` - Gemini AI integration
- ⚡ Built with asynchronous FastAPI for speed and scalability

## 🚀 Getting Started

1. **Prerequisites**
   - Python 3.8+
   - PostgreSQL
   - Gemini API key

2. **Installation**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration**
   ```bash
   # Copy example environment file
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Database Setup**
   ```bash
   # Apply migrations
   alembic upgrade head
   ```

5. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

## 🔌 API Usage

### Generate Code
```http
POST /api/v1/generator/generate
Content-Type: application/json

{
    "prompt": "Create a user authentication service",
    "context": {
        "framework": "fastapi",
        "database": "postgresql"
    }
}
```

## 🔄 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## 🔐 Environment Variables

```env
# PostgreSQL Settings
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=microweaver

# JWT Settings
SECRET_KEY=your_secret_key_here

# Gemini API Settings
GEMINI_API_KEY=your_gemini_api_key_here
```

## 📚 Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.