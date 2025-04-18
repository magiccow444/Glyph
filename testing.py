import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Start webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert the frame color (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    result = hands.process(rgb_frame)

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                gesture = None

                # Get relevant y-values
                thumb_y = hand_landmarks.landmark[4].y
                wrist_y = hand_landmarks.landmark[0].y
                index_y = hand_landmarks.landmark[8].y
                middle_y = hand_landmarks.landmark[12].y
                ring_y = hand_landmarks.landmark[16].y
                pinky_y = hand_landmarks.landmark[20].y

                # Thumbs up condition
                if (thumb_y < wrist_y and  # Thumb is above wrist
                    index_y < wrist_y and
                    pinky_y > wrist_y):
                    gesture = "Thumbs Up!"

                if gesture:
                    cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Tracker", frame)

    # Break with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
