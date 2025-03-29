import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define gesture-to-letter mapping (example for ASL letters)
GESTURE_TO_LETTER = {
    "Thumb_Up": "A",
    "Peace": "B",
    # Add more gestures and their corresponding letters here
}


def recognize_gesture(hand_landmarks):
    """Recognize gesture based on hand landmarks."""
    if hand_landmarks:
        # Example: Use specific landmarks to identify gestures
        # (You can implement custom logic here based on your dataset)
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Example condition: Thumb tip above index tip -> "Thumb_Up"
        if thumb_tip.y < index_tip.y:
            return "Thumb_Up"
        else:
            return "Unknown"

    return None


def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Use MediaPipe Hands for gesture recognition
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
    ) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break

            # Flip the frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            results = hands.process(rgb_frame)

            # Recognize gesture and map to letter
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = recognize_gesture(hand_landmarks)
                    letter = GESTURE_TO_LETTER.get(gesture, "Unknown")

                    # Display the recognized letter on the frame
                    cv2.putText(frame, f"Letter: {letter}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Draw hand landmarks on the frame
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Show the processed frame
            cv2.imshow("Gesture Recognition", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()