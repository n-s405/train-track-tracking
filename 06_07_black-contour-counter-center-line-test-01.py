import cv2
import numpy as np
import copy  

vc = cv2.VideoCapture(0)
cv2.namedWindow("hsv")
contour_counter = 0 

counter_01 = 0 
counter_02 = 0 




while True:
    _,frame= vc.read()
    
    contour_counter  = 0 
    #BASIC PROCESSING 
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",hsv)
    

    #COLOR BASED MASKING
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([1800, 255, 40])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow("Mask", mask)
 
    #CONTOURING 
    new_frame = frame.copy()
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv2.contourArea(c)
 
        if area > 5000:
            cv2.drawContours(new_frame, c, -1, (0, 255, 0), 3)
            contour_counter  += 1
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            # draw the contour and center of the shape on the image
            cv2.drawContours(new_frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(new_frame, (cX, cY), 7, (255, 255, 255), -1)
            print(cX , end=' ')
            print(cY)
            if 600<cY<650 and 500<cX<800:
                counter_01+=1
            if 650 <cY <700  and 500<cX<800:
                counter_02+=1
            # cv2.putText(new_frame2, "center", (cX - 20, cY - 20),
            #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2) 
    cv2.line(new_frame,(0,600),(2000,600),(255,255,0),4)
    cv2.line(new_frame,(0,650),(2000,650),(255,100,0),4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(new_frame,'number of contour blocks '+str(contour_counter) , (0,130),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(new_frame,'counter1 '+str(counter_01) , (0,70),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(new_frame,'counter2 '+str(counter_02) , (0,90),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.imshow("Frame", new_frame)
    print(contour_counter)
    
        
    key = cv2.waitKey(1)
    if key == 27:
        break
 
vc.release()
cv2.destroyAllWindows()