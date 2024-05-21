import numpy as np
from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_val_score
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier

# Load your data
X_train, y_train, X_val, y_val = load_data()

# Define the hyperparameter space
pbounds = {
    'num_hidden_layers': (1, 5),
    'num_neurons': (32, 512),
    'dropout_rate': (0.0, 0.5),
    'learning_rate': (1e-4, 1e-1),
}

# Define the objective function
def objective(num_hidden_layers, num_neurons, dropout_rate, learning_rate):
    def create_model():
        model = Sequential()
        model.add(Dense(num_neurons, input_dim=X_train.shape[1], activation='relu'))
        model.add(Dropout(dropout_rate))
        for _ in range(int(num_hidden_layers) - 1):
            model.add(Dense(num_neurons, activation='relu'))
            model.add(Dropout(dropout_rate))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    model = KerasClassifier(build_fn=create_model, epochs=100, batch_size=32, verbose=0)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    return -np.mean(scores)  # We want to maximize accuracy, so we return the negative mean

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
