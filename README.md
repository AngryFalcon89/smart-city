# Smart City Monitoring System

## Overview

The **Smart City Monitoring System** is a centralized solution designed to process and display real-time data from multiple Raspberry Pi modules deployed across the city. The system currently supports three modules:

1. **ANPR (Automatic Number Plate Recognition):**  
   Receives a JSON payload containing the extracted license plate number along with a license plate image.

2. **Crash Detection:**  
   Receives a short video clip of a crash event. When a crash video is received, the system triggers a notification.

3. **Face Recognition for Identity Verification:**  
   Receives an image of a person along with personal information (e.g., name, DOB) for identity recognition at government offices.

## Architecture

- **Raspberry Pi Modules:**  
  Each Raspberry Pi module is configured for a specific task (ANPR, Crash Detection, or Face Recognition). They send data to the central backend using HTTP POST requests (or via an MQTT publisher/subscriber model if preferred).

- **Centralized Backend (FastAPI):**  
  A single backend aggregates data from all modules through dedicated endpoints and processes the data accordingly. It also triggers notifications (for example, when a crash video is received).

- **Frontend Dashboard (PyQt5):**  
  The dashboard connects to the backend to display live video streams, recent ANPR results, crash notifications, and face recognition details.

## Project Structure

```
smart_city_project/
├── backend/
│   ├── models/
│   │   ├── anpr_model.py          # Schema/model for ANPR data
│   │   ├── crash_model.py         # Schema/model for crash detection data
│   │   └── face_recognition_model.py  # Schema/model for face recognition data
│   │
│   ├── routes/
│   │   ├── anpr_routes.py         # Endpoints for the ANPR module
│   │   ├── crash_routes.py        # Endpoints for the Crash Detection module
│   │   └── face_recognition_routes.py  # Endpoints for the Face Recognition module
│   │
│   ├── services/
│   │   ├── anpr_service.py        # Business logic for processing ANPR data
│   │   ├── crash_service.py       # Business logic for processing crash videos and triggering notifications
│   │   └── face_recognition_service.py  # Business logic for processing face recognition data
│   │
│   ├── main.py                    # FastAPI application entry point
│   └── config.py                  # Configuration settings (DB, notifications, etc.)
│
├── frontend/
│   ├── assets/
│   │   ├── icons/                 # UI icons
│   │   └── images/                # UI images
│   │
│   ├── components/
│   │   ├── video_widget.py        # Widget for displaying live video (if needed)
│   │   ├── anpr_widget.py         # Widget for displaying ANPR results and images
│   │   ├── notification_widget.py # Widget for displaying crash notifications
│   │   └── face_recognition_widget.py  # Widget for displaying face recognition data
│   │
│   ├── styles/
│   │   └── themes.py              # UI theme settings
│   │
│   └── dashboard.py               # Main PyQt5 dashboard
│
├── scripts/
│   ├── setup_db.py                # Script to initialize the database (if used)
│   └── run_server.sh              # Shell script to start the FastAPI server
│
├── README.md                      # Project documentation (this file)
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore settings
```

## Installation & Setup

### 1. Install Dependencies

Install the required Python packages using the provided `requirements.txt` file:

```
pip install -r requirements.txt
```

### 2. Run the Backend Server

Navigate to the `backend` directory and start the FastAPI server:

```
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### 3. Run the Frontend Dashboard

Navigate to the `frontend` directory and start the PyQt5 dashboard:

```
cd frontend
python dashboard.py
```

## API Endpoints

The backend exposes the following endpoints for the Raspberry Pi modules:

- **ANPR Endpoint:**  
  - **URL:** `/api/anpr`  
  - **Method:** POST  
  - **Payload:** JSON containing the license plate number and the license plate image (e.g., encoded in base64).

- **Crash Detection Endpoint:**  
  - **URL:** `/api/crash`  
  - **Method:** POST  
  - **Payload:** A short video clip file (multipart form-data).  
  - **Action:** Triggers a notification when a crash video is received.

- **Face Recognition Endpoint:**  
  - **URL:** `/api/face`  
  - **Method:** POST  
  - **Payload:** An image file of a person along with personal information (name, DOB, etc.).

## Future Enhancements

- **Database Integration:**

