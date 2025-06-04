# Example: utils/data_loader.py
import os
import pandas as pd

def load_data(data_dir, file_name):
    """
    Load data from a CSV file.

    Parameters:
    data_dir (str): Directory where the data file is located.
    file_name (str): Name of the data file.

    Returns:
    pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    file_path = os.path.join(data_dir, file_name)
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """
    Preprocess the data.

    Parameters:
    data (pd.DataFrame): Data to preprocess.

    Returns:
    pd.DataFrame: Preprocessed data.
    """
    # Example preprocessing steps
    data = data.dropna()  # Remove missing values
    data = data.reset_index(drop=True)  # Reset index
    return data

# Example usage
if __name__ == "__main__":
    data_dir = "path/to/data"
    file_name = "data.csv"
    data = load_data(data_dir, file_name)
    preprocessed_data = preprocess_data(data)
    print(preprocessed_data.head())
