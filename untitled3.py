import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
from sklearn.metrics import average_precision_score

# Assuming you have your data loaded as X (features) and y (target)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Define the objective function for hyperparameter tuning
def objective(params):
    params = {'max_depth': int(params['max_depth']),
              'num_leaves': int(params['num_leaves']),
              'min_child_samples': int(params['min_child_samples']),
              'max_bin': int(params['max_bin']),
              'reg_alpha': params['reg_alpha'],
              'reg_lambda': params['reg_lambda'],
              'min_child_weight': params['min_child_weight'],
              'colsample_bytree': params['colsample_bytree'],
              'subsample': params['subsample']}
    
    # Set class weights
    class_weights = {0: 1, 1: len(y_train) / sum(y_train)}  # Adjust this based on your class distribution
    
    model = LGBMClassifier(**params, n_estimators=1000, class_weight=class_weights, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=50, verbose=False)
    
    y_pred = model.predict_proba(X_test)[:, 1]
    score = average_precision_score(y_test, y_pred)
    
    return {'loss': -score, 'status': STATUS_OK}

# Define the search space for hyperparameters
space = {'max_depth': hp.quniform('max_depth', 2, 10, 1),
         'num_leaves': hp.quniform('num_leaves', 20, 200, 1),
         'min_child_samples': hp.quniform('min_child_samples', 20, 200, 1),
         'max_bin': hp.quniform('max_bin', 200, 500, 1),
         'reg_alpha': hp.uniform('reg_alpha', 0, 1),
         'reg_lambda': hp.uniform('reg_lambda', 0, 1),
         'min_child_weight': hp.uniform('min_child_weight', 1e-5, 10),
         'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1),
         'subsample': hp.uniform('subsample', 0.5, 1)}

# Perform Bayesian Optimization
trials = Trials()
best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100, trials=trials)

# Print the best hyperparameters
print('Best hyperparameters:')
print(best)
