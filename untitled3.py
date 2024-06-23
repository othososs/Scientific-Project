params = {
        'n_estimators': int(pbounds['n_estimators'][int(n_estimators)]),
        'max_depth': int(pbounds['max_depth'][int(max_depth)]),
        'learning_rate': pbounds['learning_rate'][int(learning_rate)],
        'num_leaves': int(pbounds['num_leaves'][int(num_leaves)]),
        'min_child_samples': int(pbounds['min_child_samples'][int(min_child_samples)]),
        'subsample': pbounds['subsample'][int(subsample)],
        'colsample_bytree': pbounds['colsample_bytree'][int(colsample_bytree)],
        'scale_pos_weight': scale_pos_weight * pbounds['scale_pos_weight_mult'][int(scale_pos_weight_mult)],
        'random_state': 42
    }
