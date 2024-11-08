import tensorflow as tf
from data_preprocessing import load_data, preprocess_data, split_data

def build_model(input_shape):
model = tf.keras.models.Sequential([
tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
tf.keras.layers.MaxPooling2D((2, 2)),
tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
tf.keras.layers.MaxPooling2D((2, 2)),
tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
tf.keras.layers.MaxPooling2D((2, 2)),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(512, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
return model

if __name__ == "__main__":
data_dir = 'path/to/your/data'
data = preprocess_data(data_dir)

model = build_model((150, 150, 3))
model.fit(data, epochs=10, steps_per_epoch=100, validation_steps=50)
model.save('kubu_hai_model.h5')
model = build_model((X_train.shape[1],))
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
model.save('kubu_hai_model.h5')
