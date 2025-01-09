import cv2
import time
import mediapipe as mp 

class handdetector():
    def __init__(self, mode = False, maxhands = 2, detectionconf = 0.5, trackconf = 0.5):
        self.mode = mode
        self.maxhands=maxhands
        self.detectionconf=detectionconf
        self.trackconf=trackconf

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(static_image_mode=self.mode, max_num_hands=self.maxhands,
                               model_complexity=1, min_detection_confidence=self.detectionconf,
                               min_tracking_confidence=self.trackconf)
        self.mpdraw = mp.solutions.drawing_utils

    def findhands(self, img, draw = True):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRgb)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handLm, self.mpHand.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw=True):
        
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 7, (0, 0, 0), cv2.FILLED)
        return lmList

def main():
    cTime, pTime = 0,0
    cap = cv2.VideoCapture(0)
    detector = handdetector()
    while True:

        success, img = cap.read()
        img = detector.findhands(img)
        lmList=detector.findPosition(img)
        if len(lmList) !=0:
            print(lmList[4])
        cTime = time.time()
        FPS = 1/(cTime-pTime)
        pTime=cTime

        cv2.imshow("Video", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
