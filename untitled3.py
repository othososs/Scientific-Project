from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import numpy as np
import pickle
import fsspec
import os

# Supposez que X_train et y_train sont déjà définis

# Séparation des données en ensembles d'entraînement et de validation
X_train_split, X_valid_split, y_train_split, y_valid_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

global_iteration = 0

def rf_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    
    model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
    model.fit(X_train_split, y_train_split)
    
    # Évaluer sur l'ensemble d'entraînement
    train_preds = model.predict_proba(X_train_split)[:, 1]
    train_auc = roc_auc_score(y_train_split, train_preds)
    
    # Évaluer sur l'ensemble de validation
    valid_preds = model.predict_proba(X_valid_split)[:, 1]
    valid_auc = roc_auc_score(y_valid_split, valid_preds)
    
    print(f"Iteration {global_iteration}: Train AUC = {train_auc}, Valid AUC = {valid_auc}, Params = {params}")
    
    return {'loss': -valid_auc, 'status': STATUS_OK, 'params': params}

space = {
    'n_estimators': hp.choice('n_estimators', range(50, 300)),
    'max_depth': hp.choice('max_depth', range(5, 30)),
    'min_samples_split': hp.choice('min_samples_split', range(2, 20)),
    'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 20)),
    'max_features': hp.choice('max_features', ['sqrt', 'log2', None]),
    'bootstrap': hp.choice('bootstrap', [True, False])
}

trials = Trials()
best = fmin(fn=rf_cv_evaluator,
            space=space,
            algo=tpe.suggest,
            max_evals=50,
            trials=trials)

# Entraîner le modèle avec les meilleurs hyperparamètres trouvés
best_params = trials.best_trial['result']['params']

print("Meilleurs hyperparamètres trouvés: ", best_params)

model = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1)
model.fit(X_train_split, y_train_split)

# Sauvegarder le modèle et les meilleurs hyperparamètres
path_saving = 'path/to/cloud/directory'

# Sauvegarder le modèle Random Forest
with fsspec.open(os.path.join(path_saving, 'random_forest_model.pkl'), 'wb') as f:
    pickle.dump(model, f)

# Sauvegarder les meilleurs hyperparamètres
with fsspec.open(os.path.join(path_saving, 'best_rf_params.pkl'), 'wb') as f:
    pickle.dump(best_params, f)

print("Modèle et hyperparamètres sauvegardés avec succès.")

# Charger le modèle et les hyperparamètres
with fsspec.open(os.path.join(path_saving, 'random_forest_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with fsspec.open(os.path.join(path_saving, 'best_rf_params.pkl'), 'rb') as f:
    best_params = pickle.load(f)

print("Modèle et paramètres chargés avec succès.")
print("Meilleurs hyperparamètres: ", best_params)

# Vérifier l'overfitting
train_preds = model.predict_proba(X_train_split)[:, 1]
train_auc = roc_auc_score(y_train_split, train_preds)
valid_preds = model.predict_proba(X_valid_split)[:, 1]
valid_auc = roc_auc_score(y_valid_split, valid_preds)

print(f"Performance finale - Train AUC: {train_auc}, Valid AUC: {valid_auc}")
