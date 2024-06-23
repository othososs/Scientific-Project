import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from bayes_opt import BayesianOptimization

# Load your dataset (replace this with your actual data loading code)
# Assuming X is your feature matrix and y is your target variable
# X = pd.read_csv('your_dataset.csv')
# y = X.pop('target_column')

# For demonstration purposes, let's create a dummy dataset
np.random.seed(42)
X = np.random.rand(8000000, 10)  # 8 million rows, 10 features
y = np.random.choice([0, 1], size=8000000, p=[0.95, 0.05])  # Imbalanced dataset: 95% class 0, 5% class 1

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Calculate scale_pos_weight
scale_pos_weight = np.sum(y_train == 0) / np.sum(y_train == 1)

def lgb_f1_score(n_estimators, max_depth, learning_rate, num_leaves, min_child_samples, subsample, colsample_bytree, scale_pos_weight_mult):
    params = {
        'n_estimators': int(n_estimators),
        'max_depth': int(max_depth),
        'learning_rate': learning_rate,
        'num_leaves': int(num_leaves),
        'min_child_samples': int(min_child_samples),
        'subsample': max(min(subsample, 1), 0),
        'colsample_bytree': max(min(colsample_bytree, 1), 0),
        'scale_pos_weight': scale_pos_weight * scale_pos_weight_mult,
        'random_state': 42
    }
    
    model = LGBMClassifier(**params)
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    return f1_score(y_test, predictions)

# Define the parameter space
pbounds = {
    'n_estimators': (100, 1000),
    'max_depth': (3, 10),
    'learning_rate': (0.01, 0.3),
    'num_leaves': (20, 200),
    'min_child_samples': (1, 100),
    'subsample': (0.5, 1.0),
    'colsample_bytree': (0.5, 1.0),
    'scale_pos_weight_mult': (0.5, 2.0)
}

# Initialize the optimizer
optimizer = BayesianOptimization(
    f=lgb_f1_score,
    pbounds=pbounds,
    random_state=42,
    verbose=2
)

# Run the optimization
optimizer.maximize(init_points=5, n_iter=50)

# Print the best parameters and score
print("Best parameters:", optimizer.max['params'])
print("Best F1 score:", optimizer.max['target'])

# Train the final model with the best parameters
best_params = optimizer.max['params']
best_params['n_estimators'] = int(best_params['n_estimators'])
best_params['max_depth'] = int(best_params['max_depth'])
best_params['num_leaves'] = int(best_params['num_leaves'])
best_params['min_child_samples'] = int(best_params['min_child_samples'])
best_params['scale_pos_weight'] = scale_pos_weight * best_params.pop('scale_pos_weight_mult')

final_model = LGBMClassifier(**best_params, random_state=42)
final_model.fit(X_train_scaled, y_train)

# Evaluate the model on the test set
y_pred = final_model.predict(X_test_scaled)
test_f1 = f1_score(y_test, y_pred)
print("Test F1 score:", test_f1)

# Print optimization results
for i, res in enumerate(optimizer.res):
    print(f"Iteration {i+1}:")
    print(f"F1 Score: {res['target']:.4f}")
    print(f"Parameters: {res['params']}")
    print()
