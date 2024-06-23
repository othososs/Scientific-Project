import pandas as pd
import lightgbm as lgb
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import train_test_split
from skopt import BayesSearchCV
from skopt.space import Real, Integer
import numpy as np

# Load data
data = pd.read_csv('your_dataset.csv')

# Basic preprocessing
X = data.drop(columns=['target'])
y = data['target']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Define the F1 score as the metric
f1 = make_scorer(f1_score)

# Initialize the LightGBM classifier
lgb_model = lgb.LGBMClassifier(objective='binary', n_jobs=-1, random_state=42)

# Define the parameter space
param_space = {
    'num_leaves': Integer(20, 100),
    'learning_rate': Real(0.01, 0.2, prior='log-uniform'),
    'n_estimators': Integer(50, 500),
    'scale_pos_weight': Real(np.sum(y == 0) / np.sum(y == 1), np.sum(y == 0) / np.sum(y == 1)),
    'max_depth': Integer(3, 15),
    'min_child_samples': Integer(10, 100),
    'colsample_bytree': Real(0.6, 1.0),
    'subsample': Real(0.6, 1.0),
    'reg_alpha': Real(1e-8, 10.0, prior='log-uniform'),
    'reg_lambda': Real(1e-8, 10.0, prior='log-uniform')
}

# Create the BayesSearchCV object
bayes_search = BayesSearchCV(estimator=lgb_model, search_spaces=param_space, 
                             scoring=f1, cv=3, n_iter=50, verbose=2, random_state=42, n_jobs=-1)

# Fit the model and print progress
print("Starting Bayesian optimization...")
bayes_search.fit(X_train, y_train)
print("Bayesian optimization complete.")

# Get the best model from the BayesSearchCV
best_model = bayes_search.best_estimator_

# Predict on the test set
y_pred = best_model.predict(X_test)

# Calculate the F1 score
f1_test = f1_score(y_test, y_pred)
print(f"F1 Score on the test set: {f1_test:.4f}")

# Get the best hyperparameters
best_params = bayes_search.best_params_
print("Best Hyperparameters found by Bayesian optimization:")
for param_name in sorted(best_params.keys()):
    print(f"{param_name}: {best_params[param_name]}")
