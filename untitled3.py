# Train the model with the best hyperparameters
best_params = best
model = LGBMClassifier(**best_params, n_estimators=1000, class_weight=class_weights, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = model.predict_proba(X_test)[:, 1]
auprc_score = average_precision_score(y_test, y_pred)
print(f'Test AUPRC score: {auprc_score:.4f}')
