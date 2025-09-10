from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
model = Sequential([LSTM(64, input_shape=(timesteps, feats), return_sequences=False),
                    Dropout(0.2),
                    Dense(32, activation='relu'),
                    Dense(1, activation='sigmoid')])
model.compile('adam', loss='binary_crossentropy', metrics=['accuracy'])
