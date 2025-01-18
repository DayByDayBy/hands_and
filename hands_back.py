from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import mediapipe as mp
import cv2
import base64
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# MediaPipe Hand Tracking Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def decode_image(base64_image):
    """
    Decode base64-encoded image from the client.
    """
    image_data = base64.b64decode(base64_image.split(",")[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def recognize_gesture(image):
    """
    Recognize gestures using MediaPipe Hands.
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Example: Detect "Open Palm" gesture
            # (Add more gesture logic here)
            OPEN_PALM = [8, 12, 16, 20]
            if all(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in OPEN_PALM):
                return "Open Palm"
    return "Unknown Gesture"

@socketio.on("image")
def handle_image(data):
    """
    Process image sent by the client and return the gesture.
    """
    frame = decode_image(data)
    gesture = recognize_gesture(frame)
    socketio.emit("gesture", {"gesture": gesture})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
