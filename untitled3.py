import lightgbm as lgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import roc_auc_score
import numpy as np

# Votre fonction lgbm_cv_evaluator
def lgbm_cv_evaluator(params):
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
    return {'loss': -mean_auc, 'status': STATUS_OK}

# Définir l'espace de recherche des hyperparamètres
space = {
    'num_leaves': hp.choice('num_leaves', range(20, 150)),
    'max_depth': hp.choice('max_depth', range(5, 30)),
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
    'subsample': hp.uniform('subsample', 0.5, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1.0),
    'min_child_weight': hp.uniform('min_child_weight', 0.1, 10),
    'lambda_l1': hp.uniform('lambda_l1', 0.0, 1.0),  # Régularisation L1
    'lambda_l2': hp.uniform('lambda_l2', 0.0, 1.0)   # Régularisation L2
}

# Lancer l'optimisation bayésienne
trials = Trials()
best = fmin(fn=lgbm_cv_evaluator,
            space=space,
            algo=tpe.suggest,
            max_evals=100,
            trials=trials)

print("Meilleurs hyperparamètres trouvés: ", best)
