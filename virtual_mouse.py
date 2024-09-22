
import cv2
import time
import math
import numpy as np
import hand_detector as htm
import pyautogui

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

hmin = 50
hmax = 200
color = (0, 215, 255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0

pyautogui.FAILSAFE = False

def putText(img, mode, loc=(250, 450), color=(0, 255, 255)):
    cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, color, 3)

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if len(lmList) != 0:
        if lmList[tipIds[0]][1] > lmList[tipIds[0 - 1]][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers == [0, 0, 0, 0, 0] and active == 0:
            mode = 'N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and active == 0:
            mode = 'Scroll'
            active = 1
        elif (fingers == [1, 1, 0, 0, 0]) and active == 0:
            mode = 'Volume'
            active = 1
        elif fingers == [1, 1, 1, 1, 1] and active == 0:
            mode = 'Cursor'
            active = 1
            
    if mode == 'Scroll':
        active = 1
        putText(img, mode)
        cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
        if len(lmList) != 0:
            if fingers == [0, 1, 0, 0, 0]:
                putText(img, mode='U', loc=(200, 455), color=(0, 255, 0))
                pyautogui.scroll(300)
            elif fingers == [0, 1, 1, 0, 0]:
                putText(img, mode='D', loc=(200, 455), color=(0, 0, 255))
                pyautogui.scroll(-300)
            else:
                active = 0
                mode = 'N'

    if mode == 'Volume':
        active = 1
        putText(img, mode)
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
            else:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), color, 3)
                cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [hmin, hmax], [0, 1])
                pyautogui.press('volumedown', presses=int(vol * 5))

    if mode == 'Cursor':
        active = 1
        putText(img, mode)
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0, 0, 0, 0]:
            active = 0
            mode = 'N'
        else:
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                w, h = pyautogui.size()
                X = int(np.interp(x1, [110, 620], [w - 1, 0]))
                Y = int(np.interp(y1, [20, 350], [0, h - 1]))
                cv2.circle(img, (lmList[8][1], lmList[8][2]), 7, (255, 255, 255), cv2.FILLED)
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)

                if X % 2 != 0:
                    X -= X % 2
                if Y % 2 != 0:
                    Y -= Y % 2

                pyautogui.moveTo(X, Y)
                if fingers[0] == 0:
                    cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)
                    pyautogui.click()
                    putText(img, "clicked")

    cTime = time.time()
    fps = 1 / ((cTime + 0.01) - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
    cv2.imshow('Hand LiveFeed', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()