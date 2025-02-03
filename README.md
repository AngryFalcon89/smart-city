# Smart City Monitoring System

## Overview
The **Smart City Monitoring System** is designed to collect, process, and display real-time data from Raspberry Pi devices deployed in an urban setting. The system features **Automatic Number Plate Recognition (ANPR)** and **live video surveillance** capabilities. It follows a **client-server architecture**, where the Raspberry Pi acts as the backend server, and a Python-based PyQt5 dashboard serves as the frontend for monitoring.

## Features
✅ **Live Video Streaming** using RTSP
✅ **Automatic Number Plate Recognition (ANPR) Data Display**
✅ **WebSocket for real-time ANPR updates**
✅ **Auto-reconnect for RTSP streaming**
✅ **Modular & scalable architecture**

## Project Structure
```
smart_city_project/
│── backend/
│   │── models/
│   │   ├── anpr_model.py  # Database model for ANPR data
│   │   ├── video_model.py # Database model for video stream logs
│   │
│   │── routes/
│   │   ├── anpr_routes.py  # API routes for ANPR data
│   │   ├── video_routes.py # API routes for video streaming
│   │
│   │── services/
│   │   ├── anpr_service.py  # ANPR processing logic
│   │   ├── video_service.py # Video streaming logic
│   │
│   │── main.py  # FastAPI app entry point
│   │── config.py  # API keys, database URL, and config settings
│
│── frontend/
│   │── assets/
│   │   ├── icons/  # UI icons
│   │   ├── images/ # UI images
│   │
│   │── components/
│   │   ├── video_widget.py  # Live video feed widget
│   │   ├── anpr_widget.py   # ANPR display widget
│   │
│   │── styles/
│   │   ├── themes.py  # UI theme settings
│   │
│   │── dashboard.py  # Main PyQt5 dashboard
│
│── scripts/
│   │── setup_db.py  # Database initialization script
│   │── run_server.sh  # Shell script to start FastAPI server
│
│── README.md  # Project documentation
│── requirements.txt  # Dependencies list
│── .gitignore  # Git ignore settings
```

## Installation & Setup
### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Backend (FastAPI API)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### 3️⃣ Run the Frontend Dashboard (PyQt5 GUI)
```bash
cd frontend
python dashboard.py
```

## Future Enhancements
🔹 **MongoDB/PostgreSQL integration** for logging ANPR data
🔹 **WebRTC for ultra-low-latency streaming**
🔹 **Role-based authentication & security**

## License
This project is licensed under the **MIT License**.

---
Developed for Smart City applications using Raspberry Pi, OpenCV, and FastAPI 🚀

