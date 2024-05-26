import xgboost as xgb
from bayes_opt import BayesianOptimization
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# Sous-échantillonner un sous-ensemble des données pour l'optimisation
X_train_opt, X_val, y_train_opt, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Fonction d'évaluation pour l'optimisation bayésienne
def xgb_eval(max_depth, gamma, min_child_weight, subsample, colsample_bytree):
    model = xgb.XGBClassifier(max_depth=int(max_depth),
                               gamma=gamma,
                               min_child_weight=min_child_weight,
                               subsample=subsample,
                               colsample_bytree=colsample_bytree,
                               objective='binary:logistic',
                               eval_metric='auc',
                               random_state=42,
                               n_jobs=-1)  # Parallélisation sur tous les cœurs disponibles
    
    # Entraîner le modèle sur les données d'optimisation
    model.fit(X_train_opt, y_train_opt)
    
    # Évaluer le roc_auc sur les données de validation
    roc_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
    
    return roc_auc

# Définir les espaces de recherche pour les hyperparamètres
pbounds = {'max_depth': (3, 15), 'gamma': (0, 1), 'min_child_weight': (1, 10),
           'subsample': (0.5, 1), 'colsample_bytree': (0.5, 1)}

# Initialiser l'optimiseur bayésien
optimizer = BayesianOptimization(f=xgb_eval, pbounds=pbounds, random_state=42)

# Optimiser les hyperparamètres
optimizer.maximize(init_points=5, n_iter=25, acq='ei', xi=0.0)

# Obtenir les meilleurs hyperparamètres
best_params = optimizer.max['params']
print("Meilleurs hyperparamètres : ", best_params)
