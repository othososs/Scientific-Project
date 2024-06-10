import lightgbm as lgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.model_selection import train_test_split
import numpy as np

# Séparation des données en ensembles d'entraînement et de validation
X_train_split, X_valid_split, y_train_split, y_valid_split = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# Calculer le ratio des exemples négatifs sur les exemples positifs
negative_weight = sum(y_train_split == 0)
positive_weight = sum(y_train_split == 1)
scale_pos_weight = negative_weight / positive_weight

global_iteration = 0

def lgbm_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    lgbm_train = lgb.Dataset(data=X_train_split, label=y_train_split)
    lgbm_valid = lgb.Dataset(data=X_valid_split, label=y_valid_split, reference=lgbm_train)
    params['objective'] = 'binary'
    params['metric'] = ['auc', 'auc_pr']  # Ajout de 'auc_pr' comme métrique
    params['verbose'] = -1
    params['scale_pos_weight'] = scale_pos_weight
    evals_result = {}
    model = lgb.train(
        params,
        lgbm_train,
        num_boost_round=200,
        valid_sets=[lgbm_train, lgbm_valid],
        valid_names=['train', 'valid'],
        early_stopping_rounds=30,
        verbose_eval=50,
        evals_result=evals_result
    )
    valid_auc_pr = model.best_score['valid']['auc_pr']  # Récupération de l'AUC-PR
    train_auc_pr = model.best_score['train']['auc_pr']
    print(f"Iteration {global_iteration}: Train AUC-PR = {train_auc_pr}, Valid AUC-PR = {valid_auc_pr}, Params = {params}")
    print(f"Best iteration: {model.best_iteration}")
    print(f"Evals result: {evals_result}")
    return {'loss': -valid_auc_pr, 'status': STATUS_OK, 'params': params}  # Utilisation de l'AUC-PR comme critère d'optimisation

space = {
    'num_leaves': hp.choice('num_leaves', range(20, 50)),
    'max_depth': hp.choice('max_depth', range(5, 10)),
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.1),
    'subsample': hp.uniform('subsample', 0.7, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.7, 1.0),
    'min_child_weight': hp.uniform('min_child_weight', 1, 10),
    'lambda_l1': hp.uniform('lambda_l1', 0.0, 0.5),
    'lambda_l2': hp.uniform('lambda_l2', 0.0, 0.5),
    'feature_fraction': hp.uniform('feature_fraction', 0.7, 1.0),
    'bagging_fraction': hp.uniform('bagging_fraction', 0.7, 1.0),
    'bagging_freq': hp.choice('bagging_freq', range(1, 5)),
    'max_bin': hp.choice('max_bin', range(100, 150))
}

trials = Trials()
best = fmin(fn=lgbm_cv_evaluator, space=space, algo=tpe.suggest, max_evals=50, trials=trials)

# Entraîner le modèle avec les meilleurs hyperparamètres trouvés
best_params = trials.best_trial['result']['params']
best_params['objective'] = 'binary'
best_params['metric'] = ['auc', 'auc_pr']
best_params['verbose'] = -1
best_params['scale_pos_weight'] = scale_pos_weight
print("Meilleurs hyperparamètres trouvés: ", best_params)

model = lgb.train(
    best_params,
    lgb.Dataset(data=X_train_split, label=y_train_split),
    num_boost_round=500,
    valid_sets=[
        lgb.Dataset(data=X_train_split, label=y_train_split),
        lgb.Dataset(data=X_valid_split, label=y_valid_split)
    ],
    valid_names=['train', 'valid'],
    early_stopping_rounds=30,
    verbose_eval=50
)
