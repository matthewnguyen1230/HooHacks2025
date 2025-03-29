import cv2
import mediapipe as mp
import os
import csv
import numpy as np
import glob

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def extract_landmarks_from_image(image_path):
    """Extract hand landmarks from an image using MediaPipe."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return None

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark
        else:
            return None

def create_csv_from_images(data_dir, output_csv):
    """Create a CSV file containing hand landmarks and labels from images."""
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row
        header = [f'landmark_{i}_x' for i in range(21)] + \
                 [f'landmark_{i}_y' for i in range(21)] + \
                 [f'landmark_{i}_z' for i in range(21)] + \
                 ['label']
        csv_writer.writerow(header)

        # Iterate through the image folders
        for letter_folder in glob.glob(os.path.join(data_dir, '*')): # loop through the subfolders
            if os.path.isdir(letter_folder): # Check if its a directory
                letter = os.path.basename(letter_folder) # get letter from folder name

                for image_path in glob.glob(os.path.join(letter_folder, '*.jpg')): # loop through jpgs in the folder
                    landmarks = extract_landmarks_from_image(image_path)
                    if landmarks:
                        # Prepare the data row
                        row = []
                        for landmark in landmarks:
                            row.append(landmark.x)
                        for landmark in landmarks:
                            row.append(landmark.y)
                        for landmark in landmarks:
                            row.append(landmark.z)
                        row.append(letter)

                        # Write the row to the CSV file
                        csv_writer.writerow(row)

    print(f"CSV file created at {output_csv}")

if __name__ == "__main__":
    data_dir = "C:/Users/fireb/PycharmProjects/HooHacks2025/HooHacks2025/processed_combine_asl_dataset"  # ASL image directory
    output_csv = "C:/Users/fireb/PycharmProjects/HooHacks2025/HooHacks2025/data/asl_data.csv"  # Name of the CSV file to create
    create_csv_from_images(data_dir, output_csv)