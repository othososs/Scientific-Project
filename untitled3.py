import numpy as np
from catboost import CatBoostClassifier, Pool
from bayes_opt import BayesianOptimization

# Load your data
X_train, y_train, X_val, y_val = load_data()

# Create a CatBoost Pool object from your data
train_pool = Pool(data=X_train, label=y_train)
val_pool = Pool(data=X_val, label=y_val)

# Define the hyperparameter space
pbounds = {
    'max_depth': (3, 16),
    'learning_rate': (0.01, 0.5),
    'l2_leaf_reg': (1e-8, 10),
    'bagging_temperature': (0, 1),
    'random_strength': (0, 100),
    'border_count': (1, 255),
}

# Define the objective function
def objective(max_depth, learning_rate, l2_leaf_reg, bagging_temperature, random_strength, border_count):
    model = CatBoostClassifier(
        max_depth=int(max_depth),
        learning_rate=learning_rate,
        l2_leaf_reg=l2_leaf_reg,
        bagging_temperature=bagging_temperature,
        random_strength=random_strength,
        border_count=int(border_count),
        verbose=False
    )

    model.fit(train_pool, eval_set=val_pool, early_stopping_rounds=50, plot=False)
    score = model.best_score_['validation']['Logloss']
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
