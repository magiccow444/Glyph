import cv2
import mediapipe as mp
import time

# Variables
isRightHand = False
puncCounterL = 0
puncCounterR = 0
funcCounter = 0
letterCounterL = 0
letterCounterR = 0
numberCounter = 0
xLandmarks = []
yLandmarks = []
frameSection = [0, 1, 2, 3, 4, 5]
puncLHash = {"FLH" : "(", "1LH" : ")", "2LH" : "{", "3LH" : "}", "4LH" : "'", "5LH" : "\"", "🤘LH" : ":"}
puncRHash = {"FRH" : "=", "1RH" : "+", "2RH" : "-", "3RH" : "*", "4RH" : "/", "5RH" : "^", "🤘RH" : ";"}
funcHash = {"FRH" : " ", "1RH" : "\n", "2RH" : "🖨", "3RH" : "❓", "4RH" : "⁉", "5RH" : "🔀", "FLH" : "🌌"}
letterLHash = {"FLH" : "y", "1LH" : "z"}
letterRHash = {"FRH" : "a", "1RH" : "b", "2RH" : "c", "3RH" : "d", "4RH" : "e", "5RH" : "x"}
numberHash = {"FRH" : "✊", "1RH" : "☝", "2RH" : "✌", "3RH" : "🤟", "4RH" : "🖖", "5RH" : "🖐", "1LH" : "👌", "2LH" : "🤘", "3LH" : "🙏", "4LH" : "🤞"}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize time stuff
time_since_last_gest = 0
gest_interval = 1.0

# Start webcam feed
cap = cv2.VideoCapture(0)

# Gesture detection function
def detectedGesture(xLandmarks, yLandmarks, section):
    gest = None

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
    if (isRightHand):
        if (tt_y > w_y and tt_y > i3_y and tt_y > m3_y and tt_y > r3_y and tt_y > p3_y): gest = "FRH"
        elif (tt_y > w_y and tt_y < it_y and tt_y > m3_y and tt_y > r3_y and tt_y > p3_y and it_y > m2_y): gest = "1RH"
        elif (tt_y > w_y and tt_y < m2_y and tt_y > rt_y and tt_y > pt_y and r2_y < m2_y and it_y < mt_y and it_y > r2_y): gest = "2RH"
        elif (tt_y > w_y and tt_y < m2_y and tt_y > pt_y and rt_y < mt_y and it_y < mt_y and it_y > r2_y and rt_y > i3_y): gest = "3RH"
        elif (tt_y > w_y and it_y > i3_y and mt_y > m3_y and rt_y > r3_y and pt_y > p3_y and tt_x > m1_x): gest = "4RH"
        elif (tt_y > w_y and it_y > i3_y and mt_y > m3_y and rt_y > r3_y and pt_y > p3_y and tt_x < i1_x): gest = "5RH"
        elif (tt_y > w_y and it_y > i3_y and mt_y < tt_y and rt_y < tt_y and pt_y > p3_y): gest = "🤘RH"
        else: return None

    else:
        if (tt_y > w_y and tt_y > i3_y and tt_y > mt_y and tt_y > rt_y and tt_y > pt_y): gest = "FLH"
        elif (tt_y > w_y and tt_y < it_y and tt_y > m3_y and tt_y > r3_y and tt_y > p3_y and it_y > m2_y): gest = "1LH"
        elif (tt_y > w_y and tt_y < m2_y and tt_y > rt_y and tt_y > pt_y and r2_y < m2_y and it_y < mt_y and it_y > r2_y): gest = "2LH"
        elif (tt_y > w_y and tt_y < m2_y and tt_y > pt_y and rt_y < mt_y and it_y < mt_y and it_y > r2_y and rt_y > i3_y): gest = "3LH"
        elif (tt_y > w_y and it_y > i3_y and mt_y > m3_y and rt_y > r3_y and pt_y > p3_y and tt_x < m1_x): gest = "4LH"
        elif (tt_y > w_y and it_y > i3_y and mt_y > m3_y and rt_y > r3_y and pt_y > p3_y and tt_x > i1_x): gest = "5LH"
        elif (tt_y > w_y and it_y > i3_y and mt_y < tt_y and rt_y < tt_y and pt_y > p3_y): gest = "🤘LH"
        else: return None
    
    # Uses section to check which gesture means what
    match section:
        case 0:
            if gest in puncLHash: gest = puncLHash[gest]
            else: return None
        case 1:
            if gest in puncRHash: gest = puncRHash[gest]
            else: return None
        case 2:
            if gest in funcHash: gest = funcHash[gest]
            else: return None
        case 3:
            if gest in letterLHash: gest = letterLHash[gest]
            else: return None
        case 4:
            if gest in letterRHash: gest = letterRHash[gest]
            else: return None
        case 5:
            if gest in numberHash: gest = numberHash[gest]
            else: return None

    return gest
   
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

    # If hands are detected
    if result.multi_hand_landmarks:
        # Get hand landmarks for each hand detected
        for hand_landmarks in result.multi_hand_landmarks:
            # Only runs every specified seconds (So we dont just spam code off one sign)
            if cur_time - time_since_last_gest > gest_interval:
                time_since_last_gest = cur_time
                gesture = None

                # Get all the x and y coordinates of the landmarks
                for i in range(0, 21):
                    xLandmarks.append(hand_landmarks.landmark[i].x)
                for i in range(0, 21):
                    yLandmarks.append(-hand_landmarks.landmark[i].y)

                # Checks if the hand is left of right
                if (hand_landmarks.landmark[0].x * frame.shape[1] <= 320): 
                    isRightHand = False
                elif (hand_landmarks.landmark[0].x * frame.shape[1] > 320): 
                    isRightHand = True

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
                
                # Detecting a gesture based on which section it is in the frame
                if puncCounterL == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[0])
                elif puncCounterR == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[1])
                elif funcCounter == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[2])
                elif letterCounterL == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[3])
                elif letterCounterR == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[4])
                elif numberCounter == 21: gesture = detectedGesture(xLandmarks, yLandmarks, frameSection[5])

                # Reset the counters for the next frame
                puncCounterL = 0
                puncCounterR = 0
                funcCounter = 0
                letterCounterL = 0
                letterCounterR = 0
                numberCounter = 0

                # Write the predicted gesture to the screen
                if gesture:
                    if (hand_landmarks.landmark[0].x * frame.shape[1] <= 320): cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    elif (hand_landmarks.landmark[0].x * frame.shape[1] > 320): cv2.putText(frame, gesture, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    with open('example.glyph', 'a', encoding="utf-8") as f:
                        f.write(gesture)

                # print('Shape: ', frame.shape)
                # print('Size: ', frame.size)

                # Draw the hand connections
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Clear the landmark arrays for the next frame
                xLandmarks.clear()
                yLandmarks.clear()

    # Show the frame
    cv2.imshow("Glyph", frame)

    # Break with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
