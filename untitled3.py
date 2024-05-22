from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_val_score

# Define the function to optimize
def catboost_cv(num_leaves, max_depth, learning_rate, l2_leaf_reg):
    params = {
        'num_leaves': int(num_leaves),
        'max_depth': int(max_depth),
        'learning_rate': learning_rate,
        'l2_leaf_reg': l2_leaf_reg
    }
    
    model = CatBoostClassifier(**params, **best_param)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    return scores.mean()

# Define the search space
pbounds = {
    'num_leaves': (6, 102),
    'max_depth': (3, 12),
    'learning_rate': (0.01, 0.5),
    'l2_leaf_reg': (0.1, 100)
}

# Perform Bayesian optimization
optimizer = BayesianOptimization(
    f=catboost_cv,
    pbounds=pbounds,
    random_state=42,
    verbose=2
)

optimizer.maximize(init_points=5, n_iter=25)

# Get the best hyperparameters
best_params = optimizer.max['params']
num_leaves = int(best_params['num_leaves'])
max_depth = int(best_params['max_depth'])
learning_rate = best_params['learning_rate']
l2_leaf_reg = best_params['l2_leaf_reg']

# Train the model with the best hyperparameters
cat_params = {
    'num_leaves': num_leaves,
    'max_depth': max_depth,
    'learning_rate': learning_rate,
    'l2_leaf_reg': l2_leaf_reg,
    **best_param
}

model = CatBoostClassifier(**cat_params)
train_pool = Pool(X_train, y_train, cat_index)
model.fit(train_pool)

# Evaluate model on test set
y_pred = model.predict(X_test)
# Calculate appropriate performance metrics
