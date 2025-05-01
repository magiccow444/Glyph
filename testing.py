import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize time stuff
time_since_last_gest = 0
gest_interval = 2.0

# Start webcam feed
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the image for mirror effect
    frame = cv2.flip(frame, 1) # **Shape of frame is x:640, y:480**
    
    # Convert the frame color (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    result = hands.process(rgb_frame)

    # Get time
    cur_time = time.time()

    # Draw the grid for different areas
    cv2.line(frame,(213,0),(213,480),(255,0,0),1)
    cv2.line(frame,(426,0),(426,480),(255,0,0),1)
    cv2.line(frame,(0,240),(640,240),(255,0,0),1)
    
    '''
    Grid will hopefully be:
    
    0         213           426         640
    |functions | punctuation | functions |
    |----------|-------------|-----------|240
    |letters   | numbers     | letters   |480

    '''

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in enumerate(hand_landmarks.landmark):
                # Only runs every specified seconds (So we dont just spam code off one sign)
                # if cur_time - time_since_last_gest > gest_interval:
                #     time_since_last_gest = cur_time
                gesture = None

                # region Get x-values of landmarks
                w_x = hand_landmarks.landmark[0].x      # wrist
                t1_x = hand_landmarks.landmark[1].x     # thumb base
                t2_x = hand_landmarks.landmark[2].x     # thumb middle joint
                t3_x = hand_landmarks.landmark[3].x     # thumb last joint
                tt_x = hand_landmarks.landmark[4].x     # thumb tip
                i1_x = hand_landmarks.landmark[5].x     # index base
                i2_x = hand_landmarks.landmark[6].x     # index middle joint
                i3_x = hand_landmarks.landmark[7].x     # index last joint
                it_x = hand_landmarks.landmark[8].x     # index tip
                m1_x = hand_landmarks.landmark[9].x     # middle base
                m2_x = hand_landmarks.landmark[10].x    # middle middle joint
                m3_x = hand_landmarks.landmark[11].x    # middle last joint
                mt_x = hand_landmarks.landmark[12].x    # middle tip
                r1_x = hand_landmarks.landmark[13].x    # ring base
                r2_x = hand_landmarks.landmark[14].x    # ring middle joint
                r3_x = hand_landmarks.landmark[15].x    # ring last joint
                rt_x = hand_landmarks.landmark[16].x    # ring tip
                p1_x = hand_landmarks.landmark[17].x    # pinky base
                p2_x = hand_landmarks.landmark[18].x    # pinky middle joint
                p3_x = hand_landmarks.landmark[19].x    # pinky last joint
                pt_x = hand_landmarks.landmark[20].x    # pinky tip
                # endregion

                # region Get y-values of landmarks
                w_y = -hand_landmarks.landmark[0].y
                t1_y = -hand_landmarks.landmark[1].y
                t2_y = -hand_landmarks.landmark[2].y
                t3_y = -hand_landmarks.landmark[3].y
                tt_y = -hand_landmarks.landmark[4].y
                i1_y = -hand_landmarks.landmark[5].y
                i2_y = -hand_landmarks.landmark[6].y
                i3_y = -hand_landmarks.landmark[7].y
                it_y = -hand_landmarks.landmark[8].y
                m1_y = -hand_landmarks.landmark[9].y
                m2_y = -hand_landmarks.landmark[10].y
                m3_y = -hand_landmarks.landmark[11].y
                mt_y = -hand_landmarks.landmark[12].y
                r1_y = -hand_landmarks.landmark[13].y
                r2_y = -hand_landmarks.landmark[14].y
                r3_y = -hand_landmarks.landmark[15].y
                rt_y = -hand_landmarks.landmark[16].y
                p1_y = -hand_landmarks.landmark[17].y
                p2_y = -hand_landmarks.landmark[18].y
                p3_y = -hand_landmarks.landmark[19].y
                pt_y = -hand_landmarks.landmark[20].y
                # endregion           

                # Logic for calculating which gesture is detected
                if (tt_y > w_y and it_y > w_y and pt_y < w_y): gesture = "Thumbs Up!"
                elif (tt_y < w_y and it_y < w_y and pt_y > w_y): gesture = "\nThumbs Down!"
                elif (tt_y > w_y and it_y > tt_y and mt_y > it_y): gesture = "Open Hand"

                # Write the predicted gesture to the screen
                if gesture:
                    cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    with open('example.glyph', 'a') as f:
                        f.write(gesture)

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
