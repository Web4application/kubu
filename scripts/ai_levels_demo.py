# Import AI & ML libraries
import numpy as np
import tensorflow as tf
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Import database manager
import sys
sys.path.append('./scripts')  # to allow importing from scripts dir
from db_manager import insert_data

# Example 1: Reactive Machine
def reactive_machine(input_value):
    result = "Positive" if input_value > 0 else "Negative"
    insert_data("Reactive Machine", result)
    return result

# Example 2: Limited Memory
def limited_memory_model():
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = [1 if p > 0.5 else 0 for p in model.predict(X_test)]
    accuracy = accuracy_score(y_test, predictions)
    
    insert_data("Limited Memory", f"Accuracy: {accuracy:.2f}")
    return accuracy

# Example 3: Theory of Mind
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

# Example 4: General AI (GPT-2)
def general_ai_model(prompt):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    insert_data("General AI", response)
    return response

# Example 5: Self-Aware AI
def self_aware_ai():
    message = "Self-aware AI is a theoretical concept and not yet achievable with current technology."
    insert_data("Self-Aware AI", message)
    return message

# Main execution
if __name__ == "__main__":
    print("=== Logging AI Behavior to DB ===\n")
    print("1. Reactive Machine Output:", reactive_machine(5))
    print("2. Limited Memory Accuracy:", limited_memory_model())
    print("3. Theory of Mind Accuracy:", theory_of_mind_model())
    print("4. General AI Response:", general_ai_model("Will AI take over jobs?"))
    print("5. Self-Aware AI:", self_aware_ai())
