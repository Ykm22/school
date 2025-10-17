import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score

# Check GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
if device.type == "cuda":
    print(f"GPU detected: {torch.cuda.get_device_name(0)}")
else:
    print("No GPU detected, using CPU")
input("Press Enter to continue with training...")

# Load and preprocess data
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

# Handle missing values (zeros in certain columns are actually missing)
replace_zeros = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in replace_zeros:
    data[col] = data[col].replace(0, np.nan)
    data[col] = data[col].fillna(data[col].mean())

# Split features and target
X = data.drop("Outcome", axis=1).values
y = data["Outcome"].values

# Train-test split (70-30 split commonly used)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train).to(device)
y_train_tensor = torch.FloatTensor(y_train).to(device)
X_test_tensor = torch.FloatTensor(X_test).to(device)
y_test_tensor = torch.FloatTensor(y_test).to(device)

# Create data loaders
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

batch_size = 16  # Common batch size for this dataset
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


# Define neural network architecture
class DiabetesNet(nn.Module):
    def __init__(self, input_dim=8):
        super(DiabetesNet, self).__init__()
        # Architecture: 8 -> 12 -> 8 -> 1 (common in literature)
        self.fc1 = nn.Linear(input_dim, 12)
        self.fc2 = nn.Linear(12, 8)
        self.fc3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc3(x))
        return x


# Initialize model, loss, and optimizer
model = DiabetesNet().to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Common learning rate

# Training parameters
epochs = 50  # Standard for this dataset
best_accuracy = 0.0

print("\nStarting training...")
for epoch in range(epochs):
    # Training phase
    model.train()
    train_loss = 0.0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    # Evaluation phase
    model.eval()
    with torch.no_grad():
        # Training metrics
        train_outputs = model(X_train_tensor)
        train_preds = (train_outputs.squeeze() > 0.5).float()
        train_acc = accuracy_score(y_train_tensor.cpu(), train_preds.cpu())
        train_precision = precision_score(
            y_train_tensor.cpu(), train_preds.cpu(), zero_division=0
        )
        train_recall = recall_score(y_train_tensor.cpu(), train_preds.cpu())

        # Test metrics
        test_outputs = model(X_test_tensor)
        test_preds = (test_outputs.squeeze() > 0.5).float()
        test_acc = accuracy_score(y_test_tensor.cpu(), test_preds.cpu())
        test_precision = precision_score(
            y_test_tensor.cpu(), test_preds.cpu(), zero_division=0
        )
        test_recall = recall_score(y_test_tensor.cpu(), test_preds.cpu())

        # Save best model
        if test_acc > best_accuracy:
            best_accuracy = test_acc
            torch.save(model.state_dict(), "best_diabetes_model.pth")

    # Print metrics every 10 epochs
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch + 1}/{epochs}]")
        print(
            f"  Train - Loss: {train_loss / len(train_loader):.4f}, "
            f"Acc: {train_acc:.4f}, Prec: {train_precision:.4f}, Rec: {train_recall:.4f}"
        )
        print(
            f"  Test  - Acc: {test_acc:.4f}, Prec: {test_precision:.4f}, Rec: {test_recall:.4f}"
        )

# Save final model
torch.save(model.state_dict(), "final_diabetes_model.pth")

# Final evaluation
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_tensor)
    test_preds = (test_outputs.squeeze() > 0.5).float()
    final_acc = accuracy_score(y_test_tensor.cpu(), test_preds.cpu())
    final_precision = precision_score(
        y_test_tensor.cpu(), test_preds.cpu(), zero_division=0
    )
    final_recall = recall_score(y_test_tensor.cpu(), test_preds.cpu())

print("\n" + "=" * 50)
print("FINAL TEST RESULTS:")
print(f"Accuracy: {final_acc:.4f}")
print(f"Precision: {final_precision:.4f}")
print(f"Recall: {final_recall:.4f}")
print(f"\nBest accuracy achieved: {best_accuracy:.4f}")
print("Models saved as 'best_diabetes_model.pth' and 'final_diabetes_model.pth'")
