import optuna
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective(trial, X, y, n_splits=5):
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'num_leaves': trial.suggest_int('num_leaves', 10, 100),
        'learning_rate': trial.suggest_loguniform('learning_rate', 1e-3, 0.1),
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.5, 1.0),
        'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
        'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
        'scale_pos_weight': trial.suggest_loguniform('scale_pos_weight', 1, 100)  # Changé à loguniform
    }
    
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = []
    
    for train_idx, valid_idx in cv.split(X, y):
        X_train, X_valid = X[train_idx], X[valid_idx]
        y_train, y_valid = y[train_idx], y[valid_idx]
        
        model = lgb.LGBMClassifier(**params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_valid, y_valid)],
            early_stopping_rounds=50,
            verbose=0
        )
        
        y_pred = model.predict_proba(X_valid)[:, 1]
        score = roc_auc_score(y_valid, y_pred)
        scores.append(score)
    
    return np.mean(scores)

def optimize_lgbm(X, y, n_trials=100):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X, y), n_trials=n_trials)
    
    return study.best_params, study.best_value

# Exemple d'utilisation
# X, y = load_your_data()  # Chargez vos données ici
# best_params, best_score = optimize_lgbm(X, y)
# print(f"Meilleurs paramètres : {best_params}")
# print(f"Meilleur score AUC-ROC : {best_score}")

# Entraînement du modèle final
# final_model = lgb.LGBMClassifier(**best_params)
# final_model.fit(X, y)
