import cv2
import mediapipe as mp
import time

# Variables
puncCounterL = 0
puncCounterR = 0
funcCounter = 0
letterCounterL = 0
letterCounterR = 0
numberCounter = 0
xLandmarks = []
yLandmarks = []

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize time stuff
time_since_last_gest = 0
gest_interval = 2.0

# Start webcam feed
cap = cv2.VideoCapture(0)

# Gesture detection function
def detectedGesture(xLandmarks, yLandmarks):

    # region Get x-values of landmarks
    w_x = xLandmarks[0]      # wrist
    t1_x = xLandmarks[1]     # thumb base
    t2_x = xLandmarks[2]     # thumb middle joint
    t3_x = xLandmarks[3]     # thumb last joint
    tt_x = xLandmarks[4]     # thumb tip
    i1_x = xLandmarks[5]     # index base
    i2_x = xLandmarks[6]     # index middle joint
    i3_x = xLandmarks[7]     # index last joint
    it_x = xLandmarks[8]     # index tip
    m1_x = xLandmarks[9]     # middle base
    m2_x = xLandmarks[10]    # middle middle joint
    m3_x = xLandmarks[11]    # middle last joint
    mt_x = xLandmarks[12]    # middle tip
    r1_x = xLandmarks[13]    # ring base
    r2_x = xLandmarks[14]    # ring middle joint
    r3_x = xLandmarks[15]    # ring last joint
    rt_x = xLandmarks[16]    # ring tip
    p1_x = xLandmarks[17]    # pinky base
    p2_x = xLandmarks[18]    # pinky middle joint
    p3_x = xLandmarks[19]    # pinky last joint
    pt_x = xLandmarks[20]    # pinky tip
    # endregion

    # region Get y-values of landmarks
    w_y = yLandmarks[0]
    t1_y = yLandmarks[1]
    t2_y = yLandmarks[2]
    t3_y = yLandmarks[3]
    tt_y = yLandmarks[4]
    i1_y = yLandmarks[5]
    i2_y = yLandmarks[6]
    i3_y = yLandmarks[7]
    it_y = yLandmarks[8]
    m1_y = yLandmarks[9]
    m2_y = yLandmarks[10]
    m3_y = yLandmarks[11]
    mt_y = yLandmarks[12]
    r1_y = yLandmarks[13]
    r2_y = yLandmarks[14]
    r3_y = yLandmarks[15]
    rt_y = yLandmarks[16]
    p1_y = yLandmarks[17]
    p2_y = yLandmarks[18]
    p3_y = yLandmarks[19]
    pt_y = yLandmarks[20]
    # endregion           

    # Logic for calculating which gesture is detected
    if (tt_y > w_y and it_y > w_y and pt_y < w_y): return "Thumbs Up!"
    elif (tt_y < w_y and it_y < w_y and pt_y > w_y): return "Thumbs Down!"
    elif (tt_y > w_y and it_y > tt_y and mt_y > it_y): return "Open Hand"
    else: return None


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
    
    0           213           426           640
    |punctuation | functions   | punctuation |
    |------------|-------------|-------------|240
    |letters     | numbers     | letters     |480

    480 x 640

    '''

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        # if cur_time - time_since_last_gest > gest_interval:
        #     time_since_last_gest = cur_time
        for hand_landmarks in result.multi_hand_landmarks:
            # Only runs every specified seconds (So we dont just spam code off one sign)

            gesture = None

            for i in range(0, 21):
                xLandmarks.append(hand_landmarks.landmark[i].x)
            
            for i in range(0, 21):
                yLandmarks.append(-hand_landmarks.landmark[i].y)

            gesture = detectedGesture(xLandmarks, yLandmarks)
            
            # Logic for using a gesture to end the capture (Also an example to use for de-normalizing the landmark's coordinates to compare them to the video frame proportions)
            # if (tt_y > w_y and it_y > tt_y and mt_y > it_y and (-w_y * frame.shape[0]) < 240 and (w_x * frame.shape[1]) > 213 and (w_x * frame.shape[1]) < 426): 
            #     cap.release()
            #     cv2.destroyAllWindows()

            # Logic for checking which part of the grid the hand is in
            for i in range(0, 21):
                if hand_landmarks.landmark[i].x * frame.shape[1] < 213 and hand_landmarks.landmark[i].y * frame.shape[0] < 240:
                    puncCounterL += 1
                elif hand_landmarks.landmark[i].x * frame.shape[1] > 213 and hand_landmarks.landmark[i].x * frame.shape[1] < 426 and hand_landmarks.landmark[i].y * frame.shape[0] < 240:
                    funcCounter += 1
                elif hand_landmarks.landmark[i].x * frame.shape[1] > 426 and hand_landmarks.landmark[i].y * frame.shape[0] < 240:
                    puncCounterR += 1
                elif hand_landmarks.landmark[i].x * frame.shape[1] < 213 and hand_landmarks.landmark[i].y * frame.shape[0] > 240:
                    letterCounterL += 1
                elif hand_landmarks.landmark[i].x * frame.shape[1] > 213 and hand_landmarks.landmark[i].x * frame.shape[1] < 426 and hand_landmarks.landmark[i].y * frame.shape[0] > 240:
                    numberCounter += 1
                elif hand_landmarks.landmark[i].x * frame.shape[1] > 426 and hand_landmarks.landmark[i].y * frame.shape[0] > 240:
                    letterCounterR += 1
            
            # Writing an "O" on the area the hand is in completely
            if puncCounterL == 21: 
                cv2.putText(frame, "O", (106, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif puncCounterR == 21: 
                cv2.putText(frame, "O", (532, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif funcCounter == 21: 
                cv2.putText(frame, "O", (319, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif letterCounterL == 21: 
                cv2.putText(frame, "O", (106, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif letterCounterR == 21: 
                cv2.putText(frame, "O", (532, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif numberCounter == 21: 
                cv2.putText(frame, "O", (319, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            # Reset the counters for the next frame
            puncCounterL = 0
            puncCounterR = 0
            funcCounter = 0
            letterCounterL = 0
            letterCounterR = 0
            numberCounter = 0

            # Write the predicted gesture to the screen
            if gesture:
                if (hand_landmarks.landmark[0].x * frame.shape[1] <= 320): 
                    gesture = "Left Hand, " + gesture
                    cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif (hand_landmarks.landmark[0].x * frame.shape[1] > 320): 
                    gesture = "Right Hand, " + gesture
                    cv2.putText(frame, gesture, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # with open('example.glyph', 'a') as f:
                #     f.write(gesture)

            # print('Shape: ', frame.shape)
            # print('Size: ', frame.size)

            # Draw the hand connections
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Clear the landmark arrays for the next frame
            xLandmarks.clear()
            yLandmarks.clear()

    # Show the frame
    cv2.imshow("Hand Tracker", frame)

    # Break with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
