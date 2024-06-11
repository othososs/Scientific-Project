# Obtenez les meilleurs hyperparamètres de l'optimisation bayésienne
best_params = best

# Convertissez les hyperparamètres en types appropriés
best_params_int = {
    'max_depth': int(best_params['max_depth']),
    'num_leaves': int(best_params['num_leaves']),
    'min_child_samples': int(best_params['min_child_samples']),
    'max_bin': int(best_params['max_bin']),
    'reg_alpha': best_params['reg_alpha'],
    'reg_lambda': best_params['reg_lambda'],
    'min_child_weight': best_params['min_child_weight'],
    'colsample_bytree': best_params['colsample_bytree'],
    'subsample': best_params['subsample']
}

# Entraînez le modèle avec les meilleurs hyperparamètres (types appropriés)
model = LGBMClassifier(**best_params_int, n_estimators=1000, class_weight=class_weights, random_state=42)
model.fit(X_train, y_train)

# Évaluez le modèle sur l'ensemble de test
y_pred = model.predict_proba(X_test)[:, 1]
auprc_score = average_precision_score(y_test, y_pred)
print(f'Test AUPRC score: {auprc_score:.4f}')
