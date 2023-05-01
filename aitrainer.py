import cv2
import numpy as np
import time
import posemodule as pm
 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = pm.poseDetector()

count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        angle = detector.findAngle(img, 12, 14, 16)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
 
        #dumbbell curls
        color = (0, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
 
        #bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 1)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 255, 255), 2)
 
        #count
        cv2.rectangle(img, (0, 550), (180, 720), (0, 0, 0, 50), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 7,
                    (255, 255, 255), 3)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 0), 5)
 
    cv2.imshow("POSTURA", img)
    cv2.waitKey(1)