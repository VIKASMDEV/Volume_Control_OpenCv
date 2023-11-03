import mediapipe
import cv2
import time
import numpy as np
import handtrackingmodule as htm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

#cam size
wCam, hCam = 640, 720



cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)

#speaker control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
volRange = volume.GetVolumeRange()
vol = 0
minVol = volRange[0]
maxVol = volRange[1]
volbar = 400
volper=0


while True:
    success, img = cap.read()

    #Find hand
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False )

    if len(lmList) != 0:

       #filter based on size

       #find distance between index and Thumb

       #convert volume

       #reduce resolution to make it smoother

       #checck finger up
       # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2,(y1 + y2) //2

        #drawing connecting dots
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 -x1, y2-y1)  #finding length btw two fingers
        #print(length)
        #hand range 50 - 300
        #volume range (-65) - 0

        #converting the range
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volbar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])

        print(int(length), vol)
        #sending "vol" to change the volume
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    #volume bar
    cv2.rectangle(img, (50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    #output format
    cv2.putText(img,f'fps: {int(fps)}', (40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("img",img)
    cv2.waitKey(1)




