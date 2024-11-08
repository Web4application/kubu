# Import necessary libraries
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import tensorflow as tf
from transformers import pipeline

# Load dataset for prediction AI
data = load_iris()
X = data.data
y = data.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train a Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions and evaluate the Random Forest model
rf_y_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_y_pred)
print(f'Random Forest Model Accuracy: {rf_accuracy * 100:.2f}%')

# Initialize and train a K-Nearest Neighbors classifier
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

# Make predictions and evaluate the KNN model
knn_y_pred = knn_model.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_y_pred)
print(f'KNN Model Accuracy: {knn_accuracy * 100:.2f}%')

# Bagging with Random Forest
bagging_model = BaggingClassifier(base_estimator=RandomForestClassifier(), n_estimators=10, random_state=42)
bagging_model.fit(X_train, y_train)
bagging_y_pred = bagging_model.predict(X_test)
bagging_accuracy = accuracy_score(y_test, bagging_y_pred)
print(f'Bagging Model Accuracy: {bagging_accuracy * 100:.2f}%')

# Stacking with Random Forest and KNN
estimators = [
('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
('knn', KNeighborsClassifier(n_neighbors=5))
]
stacking_model = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())
stacking_model.fit(X_train, y_train)
stacking_y_pred = stacking_model.predict(X_test)
stacking_accuracy = accuracy_score(y_test, stacking_y_pred)
print(f'Stacking Model Accuracy: {stacking_accuracy * 100:.2f}%')

# Initialize an NLP model for sentiment analysis
nlp_model = pipeline('sentiment-analysis')

# Example text for sentiment analysis
text = "I love learning about AI!"
sentiment_result = nlp_model(text)
print(f'Sentiment Analysis Result: {sentiment_result}')

# Initialize an NLP model for text classification
text_classification_model = pipeline('text-classification')

# Example text for text classification
classification_text = "AI is transforming the world."
classification_result = text_classification_model(classification_text)
print(f'Text Classification Result: {classification_result}')

# TensorFlow example (optional)
# Define a simple neural network model
tf_model = tf.keras.Sequential([
tf.keras.layers.Dense(64, activation='relu', input_shape=(4,)),
tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the TensorFlow model
tf_model.compile(optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy'])

# Train the TensorFlow model
tf_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the TensorFlow model
loss, tf_accuracy = tf_model.evaluate(X_test, y_test)
print(f'TensorFlow Model Accuracy: {tf_accuracy * 100:.2f}%')
