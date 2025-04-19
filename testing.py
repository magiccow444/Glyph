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
    frame = cv2.flip(frame, 1) # **Shape of frame is x:640, y:480**
    
    # Convert the frame color (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    result = hands.process(rgb_frame)

    # Draw the grid for different areas
    cv2.line(frame,(213,0),(213,480),(255,0,0),1)
    cv2.line(frame,(426,0),(426,480),(255,0,0),1)
    cv2.line(frame,(0,240),(640,240),(255,0,0),1)

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in enumerate(hand_landmarks.landmark):
                gesture = None

                # Get relevant y-values
                thumb_y = -hand_landmarks.landmark[4].y
                wrist_y = -hand_landmarks.landmark[0].y
                index_y = -hand_landmarks.landmark[8].y
                middle_y = -hand_landmarks.landmark[12].y
                ring_y = -hand_landmarks.landmark[16].y
                pinky_y = -hand_landmarks.landmark[20].y

                # Logic for calculating which gesture is detected
                if (thumb_y > wrist_y and index_y > wrist_y and pinky_y < wrist_y): gesture = "Thumbs Up!"
                elif (thumb_y < wrist_y and index_y < wrist_y and pinky_y > wrist_y): gesture = "Thumbs Down!"
                elif (thumb_y > wrist_y and index_y > thumb_y and middle_y > index_y): gesture = "Open Hand"

                # Write the predicted gesture to the screen
                if gesture:
                    cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # print('Shape: ', frame.shape)
                # print('Size: ', frame.size)

                # Draw the hand connections
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Tracker", frame)

    # Break with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
