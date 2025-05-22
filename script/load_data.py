import pandas as pd

# Define the path to the data file
data_file_path = 'data/dataset.csv'

# Function to load data from the CSV file
def load_data(file_path):
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("No data found in the file.")
    except pd.errors.ParserError:
        print("Error parsing the data file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Load data from the specified path
df = load_data(data_file_path)
