import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
from sklearn.metrics import accuracy_score

# Supposons que vous ayez vos données chargées en X (caractéristiques) et y (cible)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définir la fonction objective pour le réglage des hyperparamètres
def objective(params):
    params = {'depth': int(params['depth']),
              'l2_leaf_reg': params['l2_leaf_reg'],
              'learning_rate': params['learning_rate'],
              'bagging_temperature': params['bagging_temperature'],
              'random_strength': params['random_strength'],
              'border_count': int(round(params['border_count']))}
    
    model = CatBoostClassifier(**params, iterations=1000, random_state=42)
    model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50, verbose=False)
    
    y_pred = model.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    
    return {'loss': -score, 'status': STATUS_OK}

# Définir l'espace de recherche pour les hyperparamètres
space = {'depth': hp.quniform('depth', 2, 10, 1),
         'l2_leaf_reg': hp.uniform('l2_leaf_reg', 1e-5, 10),
         'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.5)),
         'bagging_temperature': hp.uniform('bagging_temperature', 0.1, 1.0),
         'random_strength': hp.uniform('random_strength', 0.1, 1.0),
         'border_count': hp.quniform('border_count', 32, 512, 1)}

# Effectuer l'optimisation bayésienne
trials = Trials()
best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100, trials=trials)

# Imprimer les meilleurs hyperparamètres
print('Meilleurs hyperparamètres:')
print(best)

# Obtenez les meilleurs hyperparamètres de l'optimisation bayésienne
best_params = best

# Convertissez les hyperparamètres en types appropriés
best_params_int = {
    'depth': int(best_params['depth']),
    'border_count': int(round(best_params['border_count'])),
    'l2_leaf_reg': best_params['l2_leaf_reg'],
    'learning_rate': best_params['learning_rate'],
    'bagging_temperature': best_params['bagging_temperature'],
    'random_strength': best_params['random_strength']
}

# Entraînez le modèle avec les meilleurs hyperparamètres (types appropriés)
model = CatBoostClassifier(**best_params_int, iterations=1000, random_state=42)
model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50, verbose=False)

# Évaluez le modèle sur l'ensemble de test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Précision sur l\'ensemble de test: {accuracy:.4f}')
