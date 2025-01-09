from gettext import install
import cv2
import mediapipe as mp 
import time
import math
import numpy as np  
import ctypes
from ctypes import cast, POINTER
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import handdetector as htm
cTime, pTime = 0,0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
detector = htm.handdetector(detectionconf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

voluRange = volume.GetVolumeRange()
minvol=voluRange[0]
maxvol=voluRange[1]


while True:

    success, img = cap.read()
    img = detector.findhands(img)
    lmList=detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        #print(lmList[4], lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1), 15, (0,0,0), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (0,0,0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,0,0), 3)
        cv2.circle(img, (cx,cy), 10, (0,0,0), cv2.FILLED)

        lengt = math.hypot(x2-x1, y2-y1)


        vol=np.interp(lengt, [10,250], [minvol, maxvol])
        print(int(lengt), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if lengt<30:
            cv2.circle(img, (cx,cy), 10, (255,255,255), cv2.FILLED)

    cTime = time.time()
    FPS = 1/(cTime-pTime)
    pTime=cTime

    cv2.imshow("Video", img)
    cv2.waitKey(1)
