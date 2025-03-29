import cv2
import mediapipe as mp
import numpy as np
import joblib # for loading the model

# Load the trained model and label encoder (from previous training step)
model = joblib.load("asl_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")

# Initialize MediaPipe Hands (same as before)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def preprocess_landmarks(landmarks):
    """Preprocess the landmarks to create a feature vector matching the Kaggle dataset."""
    landmark_list = []
    for landmark in landmarks:
        landmark_list.append(landmark.x)
        landmark_list.append(landmark.y)
        landmark_list.append(landmark.z)
    return np.array(landmark_list)

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
    ) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Preprocess the landmarks
                    landmark_array = preprocess_landmarks(hand_landmarks.landmark) # Preprocess Landmarks (x,y,z in order of landmarks

                    # Reshape for the model (assuming the model expects a batch of 1)
                    landmark_array = landmark_array.reshape(1, -1)

                    # Make a prediction
                    predicted_encoded = model.predict(landmark_array)[0] # The Model Predicts
                    predicted_letter = label_encoder.inverse_transform([predicted_encoded])[0] # Decode to a Letter

                    # Display the recognized letter
                    cv2.putText(frame, f"Letter: {predicted_letter}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Draw hand landmarks on the frame
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("ASL Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()