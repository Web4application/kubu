# Example: utils/hyperparameter_tuning.py
from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(model, param_grid, X_train, y_train):
    """
    Tune hyperparameters using GridSearchCV.

    Parameters:
    model (object): Machine learning model.
    param_grid (dict): Dictionary with parameters names as keys and lists of parameter settings to try as values.
    X_train (array): Training data.
    y_train (array): Training labels.

    Returns:
    object: Best model with tuned hyperparameters.
    """
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

# Example usage
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30]
    }
    X_train = [[0, 0], [1, 1], [0, 1], [1, 0]]
    y_train = [0, 1, 0, 1]
    best_model = tune_hyperparameters(model, param_grid, X_train, y_train)
    print(best_model)
