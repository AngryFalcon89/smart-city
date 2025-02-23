import logging
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Global variables to track connections
sender_websocket = None
viewer_websockets = []

# HTML page for viewer
viewer_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Crash Detection Viewer</title>
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
        #alerts {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 0, 0, 0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            display: none;
        }
    </style>
</head>
<body>
    <h1>Crash Detection Viewer</h1>
    <div id="video-container">
        <img id="video-frame" />
        <div id="alerts">CRASH DETECTED!</div>
    </div>
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws/crash-detection?role=viewer");
        const videoFrame = document.getElementById('video-frame');
        const alertsDiv = document.getElementById('alerts');
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'frame') {
                videoFrame.src = data.data;  // Set the image source to the base64 frame
            } else if (data.type === 'alert') {
                alertsDiv.style.display = 'block';
                setTimeout(() => {
                    alertsDiv.style.display = 'none';
                }, 2000);
            }
        };
    </script>
</body>
</html>
"""

@router.websocket("/ws/crash-detection")
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
            logger.info("Sender connected")
            
            while True:
                data = await websocket.receive_text()
                logger.info(f"Received data from sender: {data}")  # Log received message
                
                # Broadcast to all viewers
                for viewer in viewer_websockets.copy():
                    try:
                        await viewer.send_text(data)
                    except:
                        viewer_websockets.remove(viewer)
                        logger.error("Viewer disconnected unexpectedly")
        else:
            viewer_websockets.append(websocket)
            logger.info("New viewer connected (total: %d)", len(viewer_websockets))
            while True:
                await websocket.receive_text()  # Keep connection alive
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        if role == "sender":
            sender_websocket = None
            logger.info("Sender disconnected")
        else:
            viewer_websockets.remove(websocket)
            logger.info("Viewer disconnected (remaining: %d)", len(viewer_websockets))
        await websocket.close()


@router.get("/viewer")
async def viewer_page():
    return HTMLResponse(viewer_html)