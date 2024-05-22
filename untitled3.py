import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from bayes_opt import BayesianOptimization

# Load your data
data = pd.read_csv('your_data.csv')
X = data.drop('target_column', axis=1)
y = data['target_column']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Split the training data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Define the Bayesian Optimization function
def catboost_cv(max_depth,
               learning_rate,
               l2_leaf_reg,
               bagging_temperature,
               random_strength):

   # Create the CatBoost classifier
   model = CatBoostClassifier(max_depth=int(max_depth),
                              learning_rate=learning_rate,
                              l2_leaf_reg=l2_leaf_reg,
                              bagging_temperature=bagging_temperature,
                              random_strength=random_strength,
                              eval_metric='Accuracy',
                              verbose=False)

   # Fit the model on the training data and evaluate on the validation data
   model.fit(X_train, y_train, eval_set=(X_val, y_val), use_best_model=True, plot=False)

   # Get the best validation score
   best_score = max(model.evals_result_['validation']['Accuracy'])

   return best_score

# Define the search space for the hyperparameters
pbounds = {'max_depth': (2, 10),
          'learning_rate': (0.01, 0.5),
          'l2_leaf_reg': (0.1, 10),
          'bagging_temperature': (0.1, 1.0),
          'random_strength': (0.1, 1.0)}

# Initialize the Bayesian Optimizer
optimizer = BayesianOptimization(f=catboost_cv,
                                pbounds=pbounds,
                                random_state=42,
                                verbose=2)

# Optimize the hyperparameters
optimizer.maximize(init_points=5, n_iter=25)

# Get the best hyperparameters
best_params = optimizer.max['params']

# Train the final model with the best hyperparameters
final_model = CatBoostClassifier(max_depth=int(best_params['max_depth']),
                                learning_rate=best_params['learning_rate'],
                                l2_leaf_reg=best_params['l2_leaf_reg'],
                                bagging_temperature=best_params['bagging_temperature'],
                                random_strength=best_params['random_strength'],
                                eval_metric='Accuracy',
                                verbose=False)

# Fit the final model on the entire training data
final_model.fit(X_train, y_train, eval_set=(X_val, y_val), use_best_model=True, plot=True)

# Evaluate the final model on the test set
test_accuracy = final_model.score(X_test, y_test)
print(f'Test Accuracy: {test_accuracy}')
