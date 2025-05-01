import cv2 as cv
import numpy as np

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
 
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    
    if event == cv.EVENT_LBUTTONDOWN:
        print("Left button clicked")
        drawing = True
        ix,iy = x,y
 
    elif event == cv.EVENT_MOUSEMOVE:
        print("Left button moved")
        if drawing == True:
            if mode == True:
                cv.rectangle(frame,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv.circle(frame,(x,y),5,(0,0,255),-1)
 
    elif event == cv.EVENT_LBUTTONUP:
        print("Left button released")
        drawing = False
        if mode == True:
            cv.rectangle(frame,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv.circle(frame,(x,y),5,(0,0,255),-1)

frame = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)

while(True):
    cv.imshow('image', frame)

    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()