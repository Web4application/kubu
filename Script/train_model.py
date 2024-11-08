import tensorflow as tf
from data_preprocessing import load_data, preprocess_data, split_data

def build_model(input_shape):
model = tf.keras.models.Sequential([
tf.keras.layers.Dense(128, activation='relu', input_shape=input_shape),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
return model

if __name__ == "__main__":
data = load_data('data.csv')
features, target = preprocess_data(data)
X_train, X_test, y_train, y_test = split_data(features, target)

model = build_model((X_train.shape[1],))
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
model.save('kubu_hai_model.h5')
