import cv2
import HandTrackingModule as htm

class HandGestureRecognizer:
    def __init__(self):
        self.hCam, self.wCam = 480, 640
        self.cap = cv2.VideoCapture(0)
        self.cap.set(4, self.hCam)
        self.cap.set(3, self.wCam)
        self.detector = htm.handDetector(detectionCon=0)
        self.last_gesture = None
        self.stable_frames = 0

    def recognize_gesture(self):
        success, img = self.cap.read()
        img = self.detector.findHands(img)
        posList = self.detector.findPosition(img, draw=False)

        result = "Unknown"  # Default value

        if len(posList) != 0:
            finger_mcp = [5, 9, 13, 17]
            finger_dip = [6, 10, 14, 18]
            finger_pip = [7, 11, 15, 19]
            finger_tip = [8, 12, 16, 20]

            fingers = []

            for id in range(4):
                if (posList[finger_tip[id]][1] + 25 < posList[finger_dip[id]][1] and posList[16][2] < posList[20][2]):
                    fingers.append(0.25)
                elif (posList[finger_tip[id]][2] > posList[finger_dip[id]][2]):
                    fingers.append(0)
                elif (posList[finger_tip[id]][2] < posList[finger_pip[id]][2]):
                    fingers.append(1)
                elif (posList[finger_tip[id]][1] > posList[finger_pip[id]][1] and posList[finger_tip[id]][1] >
                      posList[finger_dip[id]][1]):
                    fingers.append(0.5)

            # ... rest of your logic to determine the letter based on fingers ...

            if (posList[3][2] > posList[4][2]) and (posList[3][1] > posList[6][1]) and (
                    posList[4][2] < posList[6][2]) and fingers.count(0) == 4:
                result = "A"

            elif (posList[3][1] > posList[4][1]) and fingers.count(1) == 4:
                result = "B"

            elif (posList[3][1] > posList[6][1]) and fingers.count(0.5) >= 1 and (posList[4][2] > posList[8][2]):
                result = "C"

            elif (fingers[0] == 1) and fingers.count(0) == 3 and (posList[3][1] > posList[4][1]):
                result = "D"

            elif (posList[3][1] < posList[6][1]) and fingers.count(0) == 4 and posList[12][2] < posList[4][2]:
                result = "E"

            elif (fingers.count(1) == 3) and (fingers[0] == 0) and (posList[3][2] > posList[4][2]):
                result = "F"

            # ... other conditions ...

            cv2.rectangle(img, (28, 255), (178, 425), (0, 225, 0), cv2.FILLED)
            cv2.putText(img, str(result), (55, 400), cv2.FONT_HERSHEY_COMPLEX, 5, (255, 0, 0), 15)

        else:
            result = "No hands detected"

        # Introduce a delay by requiring stable frames
        if result == self.last_gesture:
            self.stable_frames += 1
        else:
            self.stable_frames = 0
            self.last_gesture = result

        cv2.imshow("Image", img) # Show video of tracking
        cv2.waitKey(1)

        if self.stable_frames >= 5:  # Require 5 stable frames
            return result
        else:
            return "Unknown"



    def run(self):
        while True:
            result = self.recognize_gesture()
            if result:
                print(f"Recognized Letter: {result}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recognizer = HandGestureRecognizer()
    recognizer.run()
