from scripts.data_processing import load_data, preprocess_data, feature_engineering
from scripts.train_model import train_model
from scripts.evaluate import evaluate_model
from scripts.reactive import react_to_input
from scripts.self_aware import self_awareness

def main():
    # Data Processing
    data = load_data('data/dataset.csv')
    data = preprocess_data(data)
    data = feature_engineering(data)

    # Training
    train_model(data)

    # Evaluation
    evaluate_model(data)

    # Reactive Behavior
    react_to_input('Hello')

    # Self-Awareness
    self_awareness()

if __name__ == "__main__":
    main()
