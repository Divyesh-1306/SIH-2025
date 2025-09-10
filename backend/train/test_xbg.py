import joblib
import numpy as np

# Load saved model and scaler
model = joblib.load("../app/models/xgb_model.pkl")
scaler = joblib.load("../app/models/scaler.pkl")

# Example input
X_sample = np.array([[120, 25, 38, 0.4, 0.6, 3.2]])  
# [rainfall_mm, temp_C, slope_angle, vibration, displacement, pore_pressure]

X_sample_scaled = scaler.transform(X_sample)
pred = model.predict(X_sample_scaled)
proba = model.predict_proba(X_sample_scaled)

print("Prediction:", pred[0])
print("Probabilities:", proba[0])

