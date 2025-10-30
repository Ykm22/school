import pickle
from sklearn.ensemble import RandomForestClassifier

with open("train_test_splits.pkl", "rb") as f:
    data = pickle.load(f)
    X_train = data["X_train"]
    y_train = data["y_train"]

print(f"Loaded training set with {len(X_train)} samples")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to 'rf_model.pkl'")
