# MicroWeaver 🧵🚀

**MicroWeaver** is a FastAPI-based full-stack application that generates microservice scaffolds from natural language prompts like:

> "Create a user management microservice with REST APIs"

It dynamically builds the file and folder structure for a complete backend microservice, packages it, and returns it as a downloadable ZIP — perfect for rapid prototyping, hackathons, and dev acceleration.

---

## ✨ Features

- 🔤 Accepts natural language prompts for microservice creation
- 📁 Dynamically creates folders and files:
  - `/app/main.py`
  - `/app/routes/*.py`
  - `/app/models/*.py`
  - `requirements.txt`
  - `Dockerfile`
  - `README.md`
- 🔧 Uses `os`, `shutil`, and `pathlib` for file handling
- 🧠 Can be extended to use AI agents to interpret and expand user intent
- 🧵 Modular architecture: separates API, logic, and utilities
- 📦 Automatically zips generated microservice for download
- ⚡ Built with asynchronous FastAPI for speed and scalability

---