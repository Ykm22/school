import numpy as np
import pickle
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)


def nested_if_classifier(X):
    """
    Features: [sepal_length, sepal_width, petal_length, petal_width]
    Returns: 0 for Versicolor, 1 for Virginica
    """
    predictions = []

    for sample in X:
        sepal_length = sample[0]
        sepal_width = sample[1]
        petal_length = sample[2]
        petal_width = sample[3]

        # Level 1: Check petal_width (most discriminative)
        if petal_width < 1.75:
            # Level 2: Check petal_length
            if petal_length < 4.95:
                pred = 0  # Versicolor
            else:
                # Level 3: Check sepal_length
                if sepal_length < 6.0:
                    pred = 0  # Versicolor
                else:
                    pred = 1  # Virginica
        else:
            # Level 2: Check petal_length
            if petal_length < 4.85:
                pred = 0  # Versicolor
            else:
                pred = 1  # Virginica

        predictions.append(pred)

    return np.array(predictions)


with open("train_test_splits.pkl", "rb") as f:
    data = pickle.load(f)
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]

print(f"Loaded test set with {len(X_test)} samples")

y_pred = nested_if_classifier(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("=" * 50)
print("NESTED IF'S APPROACH")
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
