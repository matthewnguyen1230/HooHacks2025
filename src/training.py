import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import os
import glob  # For finding all CSV files
import numpy as np

def load_data(data_folder):
    """Load landmark data from CSV files in the data folder."""
    data = []
    labels = []

    for letter_folder in glob.glob(os.path.join(data_folder, '*')): # Loop through subfolders

        if os.path.isdir(letter_folder): # Check if it's a directory
            letter = os.path.basename(letter_folder)  # Get letter from folder name
            csv_file_path = os.path.join(letter_folder, "landmarks.csv")

            if os.path.exists(csv_file_path):
                df = pd.read_csv(csv_file_path)
                # Extract features (landmark x, y, z coordinates)
                features = df.drop('label', axis=1)  # Drop the 'label' column
                data.extend(features.values.tolist())  # Convert to list of lists

                # Extract labels
                labels.extend([letter] * len(df))  # Create list of labels

    return data, labels

# Load the data
data_folder = "ASL_Dataset"
data, labels = load_data(data_folder)

# Convert labels to numerical values (if needed - scikit-learn prefers this)
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)  # numerical labels



# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels_encoded, test_size=0.2, random_state=42)

# Create an SVM classifier
model = SVC(kernel='linear', C=1)  # You can experiment with different kernels and C values

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

print(classification_report(y_test, y_pred, target_names=label_encoder.classes_)) # use class names for report