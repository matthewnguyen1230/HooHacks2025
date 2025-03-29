import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df = pd.read_csv("asl_data.csv")  # Replace with the name of your CSV file

# Separate features and labels
X = df.drop("label", axis=1)  # Drop label
y = df["label"] # assign the labels

# Convert labels to numerical values
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y) # encoded labels

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

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

# Save the model and label encoder
joblib.dump(model, "asl_model.joblib")
joblib.dump(label_encoder, "label_encoder.joblib")
print("Model and Label Encoder saved")