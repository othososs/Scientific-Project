from sklearn.utils.class_weight import compute_class_weight

# Compute class weights
class_weights = compute_class_weight('balanced', np.unique(y_train_split), y_train_split)
class_weights = dict(enumerate(class_weights))

# Create LightGBM datasets with class weights
lgbm_train = lgb.Dataset(data=X_train_split, label=y_train_split, weight=class_weights[1])
lgbm_valid = lgb.Dataset(data=X_valid_split, label=y_valid_split, weight=class_weights[1], reference=lgbm_train)

def lgbm_cv_evaluator(params):
    global global_iteration
    global_iteration += 1
    params['objective'] = 'binary'
    params['metric'] = 'auc'
    params['verbose'] = -1
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
    valid_auc = model.best_score['valid']['auc']
    train_auc = model.best_score['train']['auc']
    print(f"Iteration {global_iteration}: Train AUC = {train_auc}, Valid AUC = {valid_auc}, Params = {params}")
    print(f"Best iteration: {model.best_iteration}")
    print(f"Evals result: {evals_result}")
    return {'loss': -valid_auc, 'status': STATUS_OK, 'params': params}

# Train the model with the best hyperparameters found
best_params = trials.best_trial['result']['params']
best_params['objective'] = 'binary'
best_params['metric'] = 'auc'
best_params['verbose'] = -1
print("Best hyperparameters found: ", best_params)
model = lgb.train(
    best_params,
    lgb.Dataset(data=X_train_split, label=y_train_split, weight=class_weights[1]),
    num_boost_round=500,
    valid_sets=[
        lgb.Dataset(data=X_train_split, label=y_train_split, weight=class_weights[1]),
        lgb.Dataset(data=X_valid_split, label=y_valid_split, weight=class_weights[1])
    ],
    valid_names=['train', 'valid'],
    early_stopping_rounds=30,
    verbose_eval=50
)
