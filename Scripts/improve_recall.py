from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import numpy as np

# Example data (replace with your actual data)
X = np.random.rand(100, 5)  # 100 samples, 5 features
y = np.random.randint(0, 2, 100)  # Binary target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# Predict probabilities
y_probs = model.predict_proba(X_test)[:, 1]

# Adjust threshold
threshold = 0.3
y_pred = (y_probs >= threshold).astype(int)

# Calculate recall
recall = recall_score(y_test, y_pred)
print(f'Recall: {recall}')
