import numpy as np
import pickle
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)

with open("rf_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("train_test_splits.pkl", "rb") as f:
    data = pickle.load(f)
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]

print(f"Loaded test set with {len(X_test)} samples")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("=" * 50)
print("ML APPROACH - RANDOM FOREST")
print("Versicolor (0) vs Virginica (1)")
print("=" * 50)
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print("\nConfusion Matrix:")
print("                    Predicted")
print("                 Versicolor  Virginica")
print(f"Versicolor          {cm[0, 0]:4d}       {cm[0, 1]:4d}")
print(f"Virginica           {cm[1, 0]:4d}       {cm[1, 1]:4d}")
print("=" * 50)
