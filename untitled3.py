import lightgbm as lgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import roc_auc_score
import numpy as np

# Initialiser un compteur global pour suivre le nombre d'itérations
global_iteration = 0

# Votre fonction lgbm_cv_evaluator
def lgbm_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    
    lgbm_dataset = lgb.Dataset(data=X_train, label=y_train)
    
    # Fixation des paramètres de base et ajout des paramètres à optimiser
    params['objective'] = 'binary'
    params['metric'] = 'auc'
    params['verbose'] = -1

    # Entraînement du modèle avec cross-validation
    cv_results = lgb.cv(
        params,
        lgbm_dataset,
        num_boost_round=1000,
        nfold=5,
        early_stopping_rounds=50,
        seed=42
    )

    # Calcul de la métrique de performance à maximiser
    mean_auc = np.max(cv_results['auc-mean'])
    
    # Afficher le statut de progression
    print(f"Iteration {global_iteration}: AUC = {mean_auc}, Params = {params}")

    return {'loss': -mean_auc, 'status': STATUS_OK}

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

print("Meilleurs hyperparamètres trouvés: ", best)
