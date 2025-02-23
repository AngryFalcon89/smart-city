import logging
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
import json

router = APIRouter()
logger = logging.getLogger(__name__)

# Global variables for WebSocket connections
face_sender_websocket = None
face_viewer_websockets = []

# HTML page for the face recognition viewer
face_viewer_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Face Recognition Viewer</title>
    <style>
        #video-container {
            position: relative;
            width: 640px;
            height: 480px;
        }
        #video-frame {
            width: 100%;
            height: 100%;
        }
        #face-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h2>Face Recognition Viewer</h2>
    <div id="video-container">
        <img id="video-frame" />
    </div>
    <div id="face-container">
        <h3>Detected Face:</h3>
        <p><strong>Name:</strong> <span id="user-name">Waiting...</span></p>
        <p><strong>Phone Number:</strong> <span id="phone-number">Waiting...</span></p>
        <p><strong>Suspected:</strong> <span id="is-suspected">Waiting...</span></p>
        <p><strong>Message:</strong> <span id="suspicion-message">Waiting...</span></p>
    </div>
    
    <script>
        const ws = new WebSocket("ws://localhost:8000/api/face-recognition/ws/face?role=viewer");
        const videoFrame = document.getElementById("video-frame");
        const userName = document.getElementById("user-name");
        const phoneNumber = document.getElementById("phone-number");
        const isSuspected = document.getElementById("is-suspected");
        const suspicionMessage = document.getElementById("suspicion-message");

        ws.onopen = function() {
            console.log("WebSocket connected successfully");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.type === 'frame') {
                videoFrame.src = data.data;  // Update video frame
            } else if (data.type === 'face') {
                userName.textContent = data.user_name || "Unknown";
                phoneNumber.textContent = data.phone_number || "N/A";
                isSuspected.textContent = data.is_suspected ? "Yes" : "No";
                suspicionMessage.textContent = data.suspicion_message || "None";
            }
        };

        ws.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        ws.onclose = function() {
            console.warn("WebSocket connection closed");
        };
    </script>
</body>
</html>
"""

@router.websocket("/ws/face")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    role = websocket.query_params.get("role", "viewer")

    global face_sender_websocket, face_viewer_websockets

    try:
        if role == "sender":
            if face_sender_websocket:
                await websocket.close(code=4001)  # Prevent multiple senders
                return
            face_sender_websocket = websocket
            logger.info("Face Recognition Sender connected")

            while True:
                data = await websocket.receive_text()
                json_data = json.loads(data)  # Parse received JSON data

                # Ensure correct structure
                message = {
                    "type": json_data.get("type", "face"),
                    "user_name": json_data.get("user_name", "Unknown"),
                    "phone_number": json_data.get("phone_number", "N/A"),
                    "is_suspected": json_data.get("is_suspected", False),
                    "suspicion_message": json_data.get("suspicion_message", "None"),
                    "data": json_data.get("data", ""),
                }
                logger.info(f"Received message: {message}")

                # Send data to all viewers
                for viewer in face_viewer_websockets.copy():
                    try:
                        await viewer.send_text(json.dumps(message))
                    except WebSocketDisconnect:
                        face_viewer_websockets.remove(viewer)
                        logger.error("Viewer disconnected unexpectedly")

        else:  # Viewer role
            face_viewer_websockets.append(websocket)
            logger.info(f"New Face Recognition Viewer connected (total: {len(face_viewer_websockets)})")
            while True:
                await websocket.receive_text()  # Keep connection alive

    except WebSocketDisconnect:
        if role == "sender":
            face_sender_websocket = None
            logger.info("Face Recognition Sender disconnected")
        else:
            if websocket in face_viewer_websockets:
                face_viewer_websockets.remove(websocket)
            logger.info(f"Face Recognition Viewer disconnected (remaining: {len(face_viewer_websockets)})")
        await websocket.close()
        
@router.get("/face-viewer")
async def face_recognition_viewer_page():
    return HTMLResponse(face_viewer_html)
