import lightgbm as lgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import numpy as np
import pickle
import fsspec
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assume X_train and y_train are already defined

# Calculate class weights
num_pos = np.sum(y_train)
num_neg = len(y_train) - num_pos
scale_pos_weight = num_neg / num_pos

# Split the data into training and validation sets (75% train, 25% valid)
X_train_split, X_valid_split, y_train_split, y_valid_split = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

global_iteration = 0
results = []

def lgbm_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    
    # Convert parameters to integers where necessary
    params['num_leaves'] = int(params['num_leaves'])
    params['max_depth'] = int(params['max_depth'])
    params['bagging_freq'] = int(params['bagging_freq'])
    params['max_bin'] = int(params['max_bin'])
    params['num_iterations'] = int(params['num_iterations'])

    # Add default LightGBM parameters
    params['objective'] = 'binary'
    params['metric'] = 'binary_logloss'  # Use log loss for training
    params['verbose'] = -1

    model = lgb.LGBMClassifier(**params, n_estimators=params['num_iterations'])

    model.fit(X_train_split, y_train_split, eval_set=[(X_valid_split, y_valid_split)],
              early_stopping_rounds=30, verbose=False)

    valid_pred = model.predict(X_valid_split)
    train_pred = model.predict(X_train_split)

    valid_f1 = f1_score(y_valid_split, valid_pred)
    train_f1 = f1_score(y_train_split, train_pred)

    print(f"Iteration {global_iteration}: Train F1 = {train_f1}, Valid F1 = {valid_f1}, Params = {params}")
    print(f"Best iteration: {model.best_iteration_}")
    
    # Save the results
    results.append({
        'iteration': global_iteration,
        'train_f1': train_f1,
        'valid_f1': valid_f1,
        'params': params
    })

    return {'loss': -valid_f1, 'status': STATUS_OK, 'params': params}

space = {
    'num_leaves': hp.choice('num_leaves', range(20, 50)),
    'max_depth': hp.choice('max_depth', range(5, 15)),
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.1),
    'subsample': hp.uniform('subsample', 0.7, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.7, 1.0),
    'min_child_weight': hp.uniform('min_child_weight', 1, 10),
    'lambda_l1': hp.uniform('lambda_l1', 0.0, 0.5),
    'lambda_l2': hp.uniform('lambda_l2', 0.0, 0.5),
    'feature_fraction': hp.uniform('feature_fraction', 0.7, 1.0),
    'bagging_fraction': hp.uniform('bagging_fraction', 0.7, 1.0),
    'bagging_freq': hp.choice('bagging_freq', range(1, 5)),
    'max_bin': hp.choice('max_bin', range(100, 150)),
    'num_iterations': hp.choice('num_iterations', range(100, 1000, 100)),
    'scale_pos_weight': hp.uniform('scale_pos_weight', 10, 7000)
}

trials = Trials()
best = fmin(fn=lgbm_cv_evaluator,
            space=space,
            algo=tpe.suggest,
            max_evals=50,
            trials=trials)

# Save the best hyperparameters
best_params = trials.best_trial['result']['params']
best_params.update({
    'objective': 'binary',
    'metric': 'binary_logloss',  # Use log loss for training
    'verbose': -1
})

print("Best hyperparameters found: ", best_params)

# Train the final model with the best hyperparameters on the complete training dataset
final_model = lgb.LGBMClassifier(**best_params, n_estimators=best_params['num_iterations'])

# Train the model on all available training data
final_model.fit(X_train, y_train)

# You can save the final model if needed
with open('final_lgbm_model.pkl', 'wb') as model_file:
    pickle.dump(final_model, model_file)

print("The final model has been trained and saved.")
