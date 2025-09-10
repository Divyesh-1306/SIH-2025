import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataset/landslide_data.csv")

# Select features
FEATURES = ["rainfall_mm", "temp_C", "slope_angle", "vibration", "displacement", "pore_pressure"]
X = df[FEATURES]
y = df["label"]
# from train.ensemble_prep import ensemble_predict
# Train-test split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numeric features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss"
)
model.fit(X_train_scaled, y_train)

# Save model and scaler
joblib.dump(model, "../app/models/xgb_model.pkl")
joblib.dump(scaler, "../app/models/scaler.pkl")

print("✅ XGBoost model trained and saved!")
