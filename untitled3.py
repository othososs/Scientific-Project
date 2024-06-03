from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
import numpy as np

# Define the hyperparameter space
param_dist = {
    'n_estimators': np.random.randint(100, 1000, 10),
    'max_depth': [None] + list(np.linspace(10, 110, num=11, dtype=int)),
    'min_samples_split': list(range(2, 21)),
    'min_samples_leaf': list(range(1, 21)),
    'max_features': ['sqrt', 'log2', None]
}

# Create the Random Forest Classifier
rf = RandomForestClassifier(random_state=42)

# Create the RandomizedSearchCV object
random_search = RandomizedSearchCV(rf, param_distributions=param_dist,
                                   n_iter=100, cv=5, scoring='accuracy',
                                   n_jobs=-1, random_state=42, verbose=3)

# Fit the RandomizedSearchCV object and print scores
random_search_results = random_search.fit(X_train, y_train)
print("Best hyperparameters: ", random_search.best_params_)
print("Best score: ", random_search.best_score_)

# Get the best model
best_model = random_search.best_estimator_
