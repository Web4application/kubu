import tensorflow as tf
from data_preprocessing import load_data, preprocess_data, split_data

def evaluate_model(model_path, X_test, y_test):
model = tf.keras.models.load_model(model_path)
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Model Loss: {loss}")
print(f"Model Accuracy: {accuracy}")

if __name__ == "__main__":
data = load_data('data.csv')
features, target = preprocess_data(data)
_, X_test, _, y_test = split_data(features, target)

evaluate_model('kubu_hai_model.h5', X_test, y_test)
