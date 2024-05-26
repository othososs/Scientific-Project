import numpy as np
import xgboost as xgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from bayes_opt import BayesianOptimization

# Chargement des données (exemple avec le jeu de données Breast Cancer)
data = load_breast_cancer()
X, y = data.data, data.target

# Liste pour stocker les scores à chaque étape
history = []

# Définition de la fonction objectif pour l'optimisation bayésienne
def xgb_cv(max_depth, learning_rate, n_estimators, gamma, min_child_weight, subsample, colsample_bytree):
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',               # Utiliser ROC AUC comme métrique d'évaluation
        'max_depth': int(max_depth),
        'learning_rate': learning_rate,
        'n_estimators': int(n_estimators),
        'gamma': gamma,
        'min_child_weight': min_child_weight,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'nthread': -1,
        'seed': 42
    }

    # Initialiser le modèle XGBoost avec les paramètres donnés
    xgb_model = xgb.XGBClassifier(**params)

    # Effectuer une validation croisée pour évaluer les performances du modèle
    cv_scores = cross_val_score(xgb_model, X, y, cv=5, scoring='roc_auc')
    mean_cv_score = np.mean(cv_scores)
    
    # Ajouter le score à l'historique
    history.append(mean_cv_score)

    # Retourner la moyenne des scores de validation croisée (la fonction objectif doit être maximisée)
    return mean_cv_score

# Définition de la fonction de rappel pour suivre la performance à chaque étape
def on_step(optim_result):
    print("Step %d - ROC AUC: %f" % (len(history), optim_result['target']))

# Définition de l'espace de recherche des hyperparamètres
xgb_bo = BayesianOptimization(
    xgb_cv,
    {
        'max_depth': (3, 10),              # Profondeur maximale de l'arbre
        'learning_rate': (0.01, 0.3),      # Taux d'apprentissage
        'n_estimators': (50, 500),         # Nombre d'arbres
        'gamma': (0, 1),                   # Valeur de réduction de perte minimale pour effectuer une division
        'min_child_weight': (1, 10),       # Poids minimal nécessaire pour créer un nouveau nœud dans l'arbre
        'subsample': (0.5, 1),             # Fraction d'échantillons à utiliser lors de la construction de chaque arbre
        'colsample_bytree': (0.5, 1)       # Fraction de caractéristiques à utiliser lors de la construction de chaque arbre
    },
    random_state=42,
    verbose=1
)

# Exécution de l'optimisation bayésienne en suivant la performance à chaque étape
xgb_bo.maximize(init_points=10, n_iter=20, acq="ei", xi=0.01, callback=on_step)

# Afficher les meilleurs paramètres
print(xgb_bo.max)
