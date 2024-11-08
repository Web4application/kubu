import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
# Load data from a CSV file
data = pd.read_csv(file_path)
return data

def preprocess_data(data):
# Handle missing values
data = data.dropna()

# Feature scaling
scaler = StandardScaler()
features = data.drop('target', axis=1)
target = data['target']
scaled_features = scaler.fit_transform(features)

return scaled_features, target

def split_data(features, target):
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
return X_train, X_test, y_train, y_test

if __name__ == "__main__":
data = load_data('data.csv')
features, target = preprocess_data(data)
X_train, X_test, y_train, y_test = split_data(features, target)
