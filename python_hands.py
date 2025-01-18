import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Define a sample gesture (e.g., Open Palm)
# A simple representation: y-coordinates of finger tips are higher than base
OPEN_PALM = [8, 12, 16, 20]  # Finger tip landmarks

def is_open_palm(hand_landmarks):
    """
    Check if the hand is in an 'open palm' position.
    """
    for finger_tip in OPEN_PALM:
        # Check if finger tip is above the base of the corresponding finger
        if hand_landmarks.landmark[finger_tip].y > hand_landmarks.landmark[finger_tip - 2].y:
            return False
    return True

# Webcam Input
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for a mirror-like view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Gesture Recognition
            if is_open_palm(hand_landmarks):
                cv2.putText(frame, "Gesture: Open Palm", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Gesture: Unknown", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("BSL Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
