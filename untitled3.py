from imblearn.under_sampling import RandomUnderSampler

# Separate features (X) and target variable (y)
X = data.drop('target', axis=1)
y = data['target']

# Initialize the random undersampler
rus = RandomUnderSampler(random_state=42)

# Perform random undersampling
X_resampled, y_resampled = rus.fit_resample(X, y)

# Print the new class distribution
print('Resampled dataset shape:', Counter(y_resampled))

from imblearn.over_sampling import MSMOTE

# Separate features (X) and target variable (y)
X = data.drop('target', axis=1)
y = data['target']

# Initialize MSMOTE
msmote = MSMOTE(random_state=42)

# Perform MSMOTE
X_resampled, y_resampled = msmote.fit_resample(X, y)

# Print the new class distribution
print('Resampled dataset shape:', Counter(y_resampled))
