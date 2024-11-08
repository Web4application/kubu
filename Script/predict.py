import tensorflow as tf
import numpy as np
from data_preprocessing import preprocess_data

def load_model(model_path):
model = tf.keras.models.load_model(model_path)
return model

def make_prediction(model, new_data):
preprocessed_data = preprocess_data(new_data)
prediction = model.predict(preprocessed_data)
return prediction

if __name__ == "__main__":
model = load_model('kubu_hai_model.h5')
new_data = np.array([[value1, value2, value3, ...]])  # Replace with actual data
prediction = make_prediction(model, new_data)
print(f"Prediction: {prediction}")
