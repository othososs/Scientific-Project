import pandas as pd
import lightgbm as lgb
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from skopt import Optimizer
from skopt.space import Real, Integer
from skopt.utils import use_named_args
import numpy as np

# Load data
data = pd.read_csv('your_dataset.csv')

# Basic preprocessing
X = data.drop(columns=['target'])
y = data['target']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Define the search space
search_space = [
    Integer(20, 100, name='num_leaves'),
    Real(0.01, 0.2, prior='log-uniform', name='learning_rate'),
    Integer(50, 500, name='n_estimators'),
    Real(np.sum(y == 0) / np.sum(y == 1), np.sum(y == 0) / np.sum(y == 1), name='scale_pos_weight'),
    Integer(3, 15, name='max_depth'),
    Integer(10, 100, name='min_child_samples'),
    Real(0.6, 1.0, name='colsample_bytree'),
    Real(0.6, 1.0, name='subsample'),
    Real(1e-8, 10.0, prior='log-uniform', name='reg_alpha'),
    Real(1e-8, 10.0, prior='log-uniform', name='reg_lambda')
]

# Initialize the optimizer
opt = Optimizer(search_space, random_state=42)

# Objective function to minimize
@use_named_args(search_space)
def objective(**params):
    model = lgb.LGBMClassifier(objective='binary', n_jobs=-1, random_state=42, **params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return -f1_score(y_test, y_pred)  # negative because we want to maximize F1

# Perform optimization
n_iter = 50
for i in range(n_iter):
    next_point = opt.ask()
    f_val = objective(**dict(zip([dim.name for dim in search_space], next_point)))
    opt.tell(next_point, f_val)
    print(f"Iteration {i+1}/{n_iter} - F1 Score: {-f_val:.4f}")

# Get the best parameters
best_params = opt.get_result().x
best_params_dict = dict(zip([dim.name for dim in search_space], best_params))

print("Best Hyperparameters found by Bayesian optimization:")
for param_name in sorted(best_params_dict.keys()):
    print(f"{param_name}: {best_params_dict[param_name]}")

# Train the final model with the best parameters
best_model = lgb.LGBMClassifier(objective='binary', n_jobs=-1, random_state=42, **best_params_dict)
best_model.fit(X_train, y_train)

# Predict on the test set
y_pred = best_model.predict(X_test)

# Calculate the F1 score
f1_test = f1_score(y_test, y_pred)
print(f"F1 Score on the test set: {f1_test:.4f}")
