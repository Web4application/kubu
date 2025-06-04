import numpy as np
import tensorflow as tf
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from db_engine import insert_data, setup_database

def reactive_machine(val):
    result = "Positive" if val > 0 else "Negative"
    insert_data("Reactive Machine", result)
    return result

def limited_memory_model():
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = [1 if p > 0.5 else 0 for p in model.predict(X_test)]

    accuracy = accuracy_score(y_test, predictions)
    insert_data("Limited Memory", f"Accuracy: {accuracy:.2f}")
    return accuracy

def theory_of_mind_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(20,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=0)
    _, accuracy = model.evaluate(X_test, y_test, verbose=0)

    insert_data("Theory of Mind", f"Accuracy: {accuracy:.2f}")
    return accuracy

def general_ai_model(prompt):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    insert_data("General AI", response)
    return response

def self_aware_ai():
    concept = "Self-aware AI is a theoretical concept and not yet achievable."
    insert_data("Self-Aware AI", concept)
    return concept

if __name__ == "__main__":
    setup_database()
    print("Reactive:", reactive_machine(5))
    print("Limited Memory Accuracy:", limited_memory_model())
    print("Theory of Mind Accuracy:", theory_of_mind_model())
    print("General AI Response:", general_ai_model("What is AI's future?"))
    print("Self-Aware AI:", self_aware_ai())
