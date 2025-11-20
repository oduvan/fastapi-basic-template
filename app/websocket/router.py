"""WebSocket endpoints."""

from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Send a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/test")
async def websocket_test_page():
    """Test page for WebSocket."""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Test</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                }
                #messages {
                    height: 400px;
                    overflow-y: scroll;
                    border: 1px solid #ccc;
                    padding: 10px;
                    margin-bottom: 10px;
                }
                .message {
                    margin: 5px 0;
                    padding: 5px;
                    background: #f5f5f5;
                    border-radius: 3px;
                }
                input, button {
                    padding: 10px;
                    font-size: 16px;
                }
                input {
                    width: 70%;
                }
                button {
                    width: 25%;
                }
            </style>
        </head>
        <body>
            <h1>WebSocket Chat Example</h1>
            <div id="messages"></div>
            <input type="text" id="messageText" placeholder="Type a message..." />
            <button onclick="sendMessage()">Send</button>
            <script>
                const ws = new WebSocket("ws://localhost:8000/ws/chat");
                const messages = document.getElementById('messages');
                const messageText = document.getElementById('messageText');

                ws.onmessage = function(event) {
                    const div = document.createElement('div');
                    div.className = 'message';
                    div.textContent = event.data;
                    messages.appendChild(div);
                    messages.scrollTop = messages.scrollHeight;
                };

                ws.onopen = function(event) {
                    const div = document.createElement('div');
                    div.className = 'message';
                    div.textContent = 'Connected to WebSocket';
                    div.style.color = 'green';
                    messages.appendChild(div);
                };

                ws.onclose = function(event) {
                    const div = document.createElement('div');
                    div.className = 'message';
                    div.textContent = 'Disconnected from WebSocket';
                    div.style.color = 'red';
                    messages.appendChild(div);
                };

                function sendMessage() {
                    const message = messageText.value;
                    if (message) {
                        ws.send(message);
                        messageText.value = '';
                    }
                }

                messageText.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.

    Clients can connect and send messages that will be broadcast to all connected clients.
    """
    await manager.connect(websocket)
    client_id = id(websocket)

    # Notify others about new connection
    await manager.broadcast(f"Client #{client_id} joined the chat")

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            # Add timestamp and client ID
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = f"[{timestamp}] Client #{client_id}: {data}"

            # Broadcast to all clients
            await manager.broadcast(message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
