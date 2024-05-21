import numpy as np
from lightgbm import LGBMClassifier
from bayes_opt import BayesianOptimization

# Load your data
X_train, y_train, X_val, y_val = load_data()

# Define the hyperparameter space
pbounds = {
    'max_depth': (3, 16),
    'num_leaves': (10, 100),
    'min_child_samples': (5, 100),
    'reg_alpha': (0.0, 1.0),
    'reg_lambda': (0.0, 1.0),
    'colsample_bytree': (0.5, 1.0),
    'subsample': (0.5, 1.0),
    'learning_rate': (0.01, 0.5),
}

# Define the objective function
def objective(max_depth, num_leaves, min_child_samples, reg_alpha, reg_lambda, colsample_bytree, subsample, learning_rate):
    model = LGBMClassifier(
        max_depth=int(max_depth),
        num_leaves=int(num_leaves),
        min_child_samples=int(min_child_samples),
        reg_alpha=reg_alpha,
        reg_lambda=reg_lambda,
        colsample_bytree=colsample_bytree,
        subsample=subsample,
        learning_rate=learning_rate,
        n_estimators=1000,
        verbose=-1
    )

    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=50, eval_metric='logloss')
    score = model.best_score_['valid_0']['logloss']
    return score

# Optimize hyperparameters
optimizer = BayesianOptimization(
    f=objective,
    pbounds=pbounds,
    random_state=42,
)

optimizer.maximize(init_points=5, n_iter=100)

# Print the best hyperparameters
print("Best hyperparameters:")
print(optimizer.max)
