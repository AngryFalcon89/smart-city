import os

def create_dirs():
    directories = [
        "backend/models",
        "backend/routes",
        "backend/services",
        "frontend/assets/icons",
        "frontend/assets/images",
        "frontend/components",
        "frontend/styles",
        "scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_files():
    files = {
        "backend/main.py": "# FastAPI main server entry point\n",
        "backend/config.py": "# Configuration settings\n",
        "backend/models/anpr_model.py": "# ANPR model\n",
        "backend/models/crash_model.py": "# Crash detection model\n",
        "backend/models/face_recognition_model.py": "# Face recognition model\n",
        "backend/routes/anpr_routes.py": "# API routes for ANPR\n",
        "backend/routes/crash_routes.py": "# API routes for Crash Detection\n",
        "backend/routes/face_recognition_routes.py": "# API routes for Face Recognition\n",
        "backend/services/anpr_service.py": "# Business logic for ANPR\n",
        "backend/services/crash_service.py": "# Business logic for Crash Detection\n",
        "backend/services/face_recognition_service.py": "# Business logic for Face Recognition\n",
        "frontend/dashboard.py": "# PyQt5 dashboard entry point\n",
        "frontend/styles/themes.py": "# UI themes\n",
        "scripts/setup_db.py": "# Script to initialize the database\n",
        "scripts/run_server.sh": "#!/bin/bash\nuvicorn backend.main:app --host 0.0.0.0 --port 5000 --reload\n",
        "requirements.txt": "fastapi\nuvicorn\nPyQt5\n",
        ".gitignore": "__pycache__/\n*.pyc\n.env\n"
    }
    
    for filepath, content in files.items():
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created file: {filepath}")

if __name__ == "__main__":
    create_dirs()
    create_files()
    print("Project structure created successfully.")
