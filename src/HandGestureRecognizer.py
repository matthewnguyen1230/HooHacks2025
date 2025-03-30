import cv2
import time
import os
import HandTrackingModule as htm

class HandGestureRecognizer:
    def __init__(self):
        self.hCam, self.wCam = 480, 660
        self.cap = cv2.VideoCapture(0)
        self.cap.set(4, self.hCam)
        self.cap.set(3, self.wCam)
        self.detector = htm.handDetector(detectionCon=0)
        self.confirmed_letter = None  # Variable to hold the confirmed letter
        self.letter_count = 0  # Counter for consecutive frames with the same letter

    def recognize_gesture(self):
        success, img = self.cap.read()
        img = self.detector.findHands(img)
        posList = self.detector.findPosition(img, draw=False)

        result = "Unknown"  # Default value

        if len(posList) != 0 and len(posList) >= 21:  # Ensure posList has enough points
            finger_mcp = [5, 9, 13, 17]
            finger_dip = [6, 10, 14, 18]
            finger_pip = [7, 11, 15, 19]
            finger_tip = [8, 12, 16, 20]

            fingers = []

            for id in range(4):
                if len(posList) > finger_tip[id] and len(posList) > finger_dip[id]:
                    if (posList[finger_tip[id]][1] + 25 < posList[finger_dip[id]][1] and posList[16][2] < posList[20][
                        2]):
                        fingers.append(0.25)
                    elif (posList[finger_tip[id]][2] > posList[finger_dip[id]][2]):
                        fingers.append(0)
                    elif (posList[finger_tip[id]][2] < posList[finger_pip[id]][2]):
                        fingers.append(1)
                    elif (posList[finger_tip[id]][1] > posList[finger_pip[id]][1] and posList[finger_tip[id]][1] >
                          posList[finger_dip[id]][1]):
                        fingers.append(0.5)

            # Ensure fingers list has enough elements
            if len(fingers) == 4:
                # ... rest of your logic to determine the letter based on fingers ...

                if (len(posList) > 3 and len(posList) > 4 and len(posList) > 6) and (
                        posList[3][2] > posList[4][2]) and (posList[3][1] > posList[6][1]) and (
                        posList[4][2] < posList[6][2]) and fingers.count(0) == 4:
                    result = "A"

                elif (len(posList) > 3 and len(posList) > 4) and (posList[3][1] > posList[4][1]) and fingers.count(
                        1) == 4:
                    result = "B"

                elif (len(posList) > 3 and len(posList) > 6 and len(posList) > 8) and (
                        posList[3][1] > posList[6][1]) and fingers.count(0.5) >= 1 and (posList[4][2] > posList[8][2]):
                    result = "C"

                elif (len(fingers) > 0 and fingers[0] == 1) and fingers.count(0) == 3 and (
                        len(posList) > 3 and len(posList) > 4) and (posList[3][1] > posList[4][1]):
                    result = "D"

                elif (len(posList) > 3 and len(posList) > 6 and len(posList) > 12) and (
                        posList[3][1] < posList[6][1]) and fingers.count(0) == 4 and posList[12][2] < posList[4][2]:
                    result = "E"

                elif (len(fingers) > 0 and fingers.count(1) == 3) and (fingers[0] == 0) and (
                        len(posList) > 3 and len(posList) > 4) and (posList[3][2] > posList[4][2]):
                    result = "F"

                # ... rest of your conditions ...

            else:
                result = "Not enough fingers detected"

        else:
            result = "N/A"

        # Display the camera feed
        cv2.putText(img, str(result), (55, 400), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 4)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # Update confirmed letter and count
        if result == self.confirmed_letter:
            self.letter_count += 1
        else:
            self.confirmed_letter = result
            self.letter_count = 1

        if self.letter_count >= 3:  # Only return confirmed letter after 3 frames
            confirmed_result = self.confirmed_letter
            self.confirmed_letter = None  # Reset confirmed letter
            self.letter_count = 0  # Reset counter
            return confirmed_result
        else:
            return "N/A"



    def run(self):
        while True:
            result = self.recognize_gesture()
            if result != "N/A":
                print(f"Recognized Letter: {result}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recognizer = HandGestureRecognizer()
    recognizer.run()
