import xgboost as xgb
from bayes_opt import BayesianOptimization
from bayes_opt.util import UtilityFunction
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# Sous-échantillonner un sous-ensemble des données pour l'optimisation
X_train_opt, X_val, y_train_opt, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Fonction de suivi des performances à chaque étape de l'entraînement
def xgb_eval_metric(y_pred, dtrain):
    labels = dtrain.get_label()
    roc_auc = roc_auc_score(labels, y_pred)
    return 'roc_auc', roc_auc

# Fonction d'évaluation pour l'optimisation bayésienne
def xgb_eval(max_depth, gamma, min_child_weight, subsample, colsample_bytree):
    params = {
        'max_depth': int(max_depth),
        'gamma': gamma,
        'min_child_weight': min_child_weight,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'random_state': 42,
        'n_jobs': -1  # Parallélisation sur tous les cœurs disponibles
    }
    
    # Convertir les données d'optimisation en DMatrix XGBoost
    dtrain_opt = xgb.DMatrix(X_train_opt, label=y_train_opt)
    dval = xgb.DMatrix(X_val, label=y_val)
    
    # Entraîner le modèle sur les données d'optimisation avec suivi des performances
    model = xgb.train(params, dtrain_opt, num_boost_round=100, evals=[(dtrain_opt, 'train'), (dval, 'val')],
                      feval=xgb_eval_metric, verbose_eval=True)
    
    # Évaluer le roc_auc final sur les données de validation
    preds = model.predict(dval)
    roc_auc = roc_auc_score(dval.get_label(), preds)
    
    return roc_auc

# Définir les espaces de recherche pour les hyperparamètres
pbounds = {'max_depth': (3, 15), 'gamma': (0, 1), 'min_child_weight': (1, 10),
           'subsample': (0.5, 1), 'colsample_bytree': (0.5, 1)}

# Initialiser l'optimiseur bayésien
optimizer = BayesianOptimization(f=xgb_eval, pbounds=pbounds, random_state=42)

# Définir la fonction d'acquisition (ici, nous utilisons la fonction EI par défaut)
utility_function = UtilityFunction(kind='ei', xi=0.0)
optimizer.set_gp_params(utility_function.gp_params)  # Définir les paramètres du processus gaussien

# Fonction de rappel pour suivre l'évolution à chaque itération
def print_iter_callback(iter_num, max_val, max_params, max_iter):
    print(f"Itération {iter_num}/{max_iter}: roc_auc = {max_val:.4f}, paramètres = {max_params}")

# Optimiser les hyperparamètres avec suivi de l'évolution
optimizer.maximize(
    init_points=5,
    n_iter=25,
    acq=utility_function.utility,
    callback=print_iter_callback,
    callback_kwargs={'max_iter': 25}
)

# Obtenir les meilleurs hyperparamètres
best_params = optimizer.max['params']
print("Meilleurs hyperparamètres : ", best_params)
