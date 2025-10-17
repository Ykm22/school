import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score

# Load data directly from URL
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]
data = pd.read_csv(url, names=columns)

# Handle missing values
replace_zeros = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in replace_zeros:
    data[col] = data[col].replace(0, np.nan)
    data[col] = data[col].fillna(data[col].mean())

X = data.drop("Outcome", axis=1).values
y = data["Outcome"].values

# Use same random_state to get same test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Storage for predictions
predictions = []

# Iterate through each patient in test set
for patient in X_test:
    pregnancies = patient[0]
    glucose = patient[1]
    blood_pressure = patient[2]
    skin_thickness = patient[3]
    insulin = patient[4]
    bmi = patient[5]
    diabetes_pedigree = patient[6]
    age = patient[7]

    # Raw if statements with thresholds found from training
    diabetes_score = 0

    if glucose > 127.20:
        diabetes_score += 1

    if bmi > 29.15:
        diabetes_score += 1

    if age > 28.00:
        diabetes_score += 1

    if diabetes_pedigree > 0.32:
        diabetes_score += 1

    if pregnancies > 3.00:
        diabetes_score += 1

    if insulin > 121.80:
        diabetes_score += 1

    if blood_pressure > 70.00:
        diabetes_score += 1

    if skin_thickness > 28.00:
        diabetes_score += 1

    # Make prediction based on majority vote
    if diabetes_score >= 4:
        prediction = 1
    else:
        prediction = 0

    predictions.append(prediction)

# Convert to numpy array
predictions = np.array(predictions)

# Calculate metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions)

print("Results using 8 IF statements:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

# Show confusion matrix details
true_positives = np.sum((predictions == 1) & (y_test == 1))
true_negatives = np.sum((predictions == 0) & (y_test == 0))
false_positives = np.sum((predictions == 1) & (y_test == 0))
false_negatives = np.sum((predictions == 0) & (y_test == 1))

print(f"\nConfusion Matrix:")
print(f"True Positives: {true_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")

# Save results
results_df = pd.DataFrame({"True_Label": y_test, "Prediction": predictions})
results_df.to_csv("pima_predictions.csv", index=False)
print(f"\nPredictions saved to 'pima_predictions.csv'")
