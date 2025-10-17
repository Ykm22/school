import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score


# Define the same model architecture
class DiabetesNet(nn.Module):
    def __init__(self, input_dim=8):
        super(DiabetesNet, self).__init__()
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


# Check device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load data from remote
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

# Split features and target
X = data.drop("Outcome", axis=1).values
y = data["Outcome"].values

# Same train-test split as training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Standardize features (fit on train, apply to test)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to PyTorch tensors
X_test_tensor = torch.FloatTensor(X_test).to(device)
y_test_tensor = torch.FloatTensor(y_test).to(device)

# Load the saved model
model = DiabetesNet().to(device)
model.load_state_dict(torch.load("best_diabetes_model.pth", map_location=device))
model.eval()

# Make predictions
with torch.no_grad():
    outputs = model(X_test_tensor)
    predictions = (outputs.squeeze() > 0.5).float()

# Calculate metrics
accuracy = accuracy_score(y_test_tensor.cpu(), predictions.cpu())
precision = precision_score(y_test_tensor.cpu(), predictions.cpu(), zero_division=0)
recall = recall_score(y_test_tensor.cpu(), predictions.cpu())

print("\n" + "=" * 50)
print("LOADED MODEL PERFORMANCE ON TEST SET:")
print("=" * 50)
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print("=" * 50)
