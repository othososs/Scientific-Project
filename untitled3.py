import lightgbm as lgb
import optuna
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

class ScorePrinter(lgb.callback.CallbackEnviroData):
    def __init__(self, val_data):
        self.val_data = val_data

    def iteration_end_cb(self, env):
        model = env.model
        val_pred = model.predict(self.val_data[0])
        val_score = f1_score(self.val_data[1], val_pred > 0.5)
        print(f"Iteration {env.iteration}, Validation F1 Score: {val_score:.4f}")

def objective(trial, X, y):
    # Définir l'espace de recherche des hyperparamètres
    max_depth = trial.suggest_int('max_depth', 2, 32)
    n_estimators = trial.suggest_int('n_estimators', 100, 1000)
    class_weight = {0: 1, 1: trial.suggest_int('class_weight_1', 50, 200)}

    # Initialiser le modèle LightGBM
    model = lgb.LGBMClassifier(max_depth=max_depth, n_estimators=n_estimators, class_weight=class_weight)

    # Validation croisée stratifiée
    scores = []
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for train_idx, val_idx in kfold.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        # Initialiser le callback pour afficher le score de validation
        callback = ScorePrinter(val_data=(X_val, y_val))

        model.fit(X_train, y_train, callbacks=[callback])
        y_pred = model.predict_proba(X_val)[:, 1]

        # Calculer la métrique (par exemple, le score F1)
        score = f1_score(y_val, y_pred > 0.5)
        scores.append(score)

    return 1 - np.mean(scores)  # Minimiser la valeur de retour

# Données d'exemple
X = ... # Vos données d'entrée
y = ... # Vos étiquettes de classe

study = optuna.create_study(direction='minimize')
study.optimize(lambda trial: objective(trial, X, y), n_trials=100)

# Récupérer les meilleurs hyperparamètres
best_params = study.best_trial.params
print(f"Meilleurs hyperparamètres: {best_params}")
