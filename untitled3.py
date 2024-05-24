import lightgbm as lgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import numpy as np
import pickle
import fsspec
import os

# Assurez-vous que X_train et y_train sont correctement définis
# Exemple :
# X_train = ...
# y_train = ...

# Séparation des données en ensembles d'entraînement et de validation
X_train_split, X_valid_split, y_train_split, y_valid_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Initialiser un compteur global pour suivre le nombre d'itérations
global_iteration = 0

# Fonction d'évaluation pour l'optimisation bayésienne
def lgbm_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    
    lgbm_train = lgb.Dataset(data=X_train_split, label=y_train_split)
    lgbm_valid = lgb.Dataset(data=X_valid_split, label=y_valid_split, reference=lgbm_train)
    
    # Fixation des paramètres de base et ajout des paramètres à optimiser
    params['objective'] = 'binary'
    params['metric'] = 'auc'
    params['verbose'] = -1

    # Entraînement du modèle avec validation
    model = lgb.train(
        params,
        lgbm_train,
        num_boost_round=1000,
        valid_sets=[lgbm_train, lgbm_valid],
        valid_names=['train', 'valid'],
        early_stopping_rounds=50,
        verbose_eval=100,
        evals_result={}
    )

    # Calcul de la métrique de performance à maximiser
    valid_auc = model.best_score['valid']['auc']
    train_auc = model.best_score['train']['auc']
    
    # Afficher le statut de progression
    print(f"Iteration {global_iteration}: Train AUC = {train_auc}, Valid AUC = {valid_auc}, Params = {params}")

    return {'loss': -valid_auc, 'status': STATUS_OK, 'params': params}

# Définir l'espace de recherche des hyperparamètres
space = {
    'num_leaves': hp.choice('num_leaves', range(20, 100)),  # Réduire le nombre de feuilles
    'max_depth': hp.choice('max_depth', range(5, 20)),  # Limiter la profondeur des arbres
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
    'subsample': hp.uniform('subsample', 0.5, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1.0),
    'min_child_weight': hp.uniform('min_child_weight', 0.1, 10),
    'lambda_l1': hp.uniform('lambda_l1', 0.0, 1.0),  # Régularisation L1
    'lambda_l2': hp.uniform('lambda_l2', 0.0, 1.0),  # Régularisation L2
    'feature_fraction': hp.uniform('feature_fraction', 0.6, 1.0),  # Utiliser un sous-ensemble de caractéristiques
    'bagging_fraction': hp.uniform('bagging_fraction', 0.6, 1.0),  # Utiliser un sous-ensemble de données
    'bagging_freq': hp.choice('bagging_freq', range(1, 10)),  # Fréquence de bagging
    'max_bin': hp.choice('max_bin', range(64, 256))  # Ajuster le nombre de bins
}

# Lancer l'optimisation bayésienne
trials = Trials()
best = fmin(fn=lgbm_cv_evaluator,
            space=space,
            algo=tpe.suggest,
            max_evals=100,
            trials=trials)

# Entraîner le modèle avec les meilleurs hyperparamètres trouvés
best_params = trials.best_trial['result']['params']
best_params['objective'] = 'binary'
best_params['metric'] = 'auc'
best_params['verbose'] = -1

model = lgb.train(
    best_params,
    lgb.Dataset(data=X_train_split, label=y_train_split),
    num_boost_round=1000,
    valid_sets=[lgb.Dataset(data=X_train_split, label=y_train_split), lgb.Dataset(data=X_valid_split, label=y_valid_split)],
    valid_names=['train', 'valid'],
    early_stopping_rounds=50
)
