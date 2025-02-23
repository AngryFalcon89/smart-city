import logging
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect

router = APIRouter()
logger = logging.getLogger(__name__)

# Global variables to track WebSocket connections
sender_websocket = None
viewer_websockets = []

# HTML page for the viewer
viewer_html = """
<!DOCTYPE html>
<html>
<head>
    <title>ANPR Viewer</title>
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
        #plate-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h2>ANPR Viewer</h2>
    <div id="video-container">
        <img id="video-frame" />
    </div>
    <div id="plate-container">
        <h3>Detected Number Plate:</h3>
        <p id="number-plate">Waiting for data...</p>
    </div>
    <script>
        const ws = new WebSocket("ws://localhost:8000/api/anpr/ws/anpr?role=viewer");
        const videoFrame = document.getElementById("video-frame");
        const plateDisplay = document.getElementById("number-plate");

        ws.onopen = function() {
            console.log("WebSocket connected successfully");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'frame') {
                videoFrame.src = data.data;  // Update video frame
            } else if (data.type === 'plate') {
                plateDisplay.textContent = data.plate;  // Update number plate display
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

@router.websocket("/ws/anpr")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    role = websocket.query_params.get("role", "viewer")
    global sender_websocket, viewer_websockets

    try:
        if role == "sender":
            if sender_websocket:
                await websocket.close(code=4001)
                return
            sender_websocket = websocket
            logger.info("ANPR Sender connected")

            while True:
                data = await websocket.receive_text()
                for viewer in viewer_websockets.copy():
                    try:
                        await viewer.send_text(data)
                    except WebSocketDisconnect:
                        viewer_websockets.remove(viewer)
                        logger.error("Viewer disconnected unexpectedly")

        else:
            viewer_websockets.append(websocket)
            logger.info(f"New ANPR Viewer connected (total: {len(viewer_websockets)})")
            while True:
                await websocket.receive_text()

    except WebSocketDisconnect:
        if role == "sender":
            sender_websocket = None
            logger.info("ANPR Sender disconnected")
        else:
            if websocket in viewer_websockets:
                viewer_websockets.remove(websocket)
            logger.info(f"ANPR Viewer disconnected (remaining: {len(viewer_websockets)})")
        await websocket.close()

@router.get("/anpr-viewer")
async def anpr_viewer_page():
    return HTMLResponse(viewer_html)
