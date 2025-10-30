import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pickle

iris = load_iris()
X = iris.data
y = iris.target

# Filter for only Versicolor (1) and Virginica (2)
mask = (y == 1) | (y == 2)
X = X[mask]
y = y[mask]

# Convert to binary: Versicolor=0, Virginica=1
y_binary = (y == 2).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_binary, test_size=0.3, random_state=42
)

with open("train_test_splits.pkl", "wb") as f:
    pickle.dump(
        {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": iris.feature_names,
        },
        f,
    )

print("Train/test splits saved to 'train_test_splits.pkl'")
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
print(
    f"Class distribution in train: Versicolor={np.sum(y_train == 0)}, Virginica={np.sum(y_train == 1)}"
)
print(
    f"Class distribution in test: Versicolor={np.sum(y_test == 0)}, Virginica={np.sum(y_test == 1)}"
)
print(f"Feature names: {iris.feature_names}")
