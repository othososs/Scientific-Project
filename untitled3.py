from collections import Counter
from imblearn.over_sampling import SMOTE
import numpy as np

# Separate features (X) and target variable (y)
X = data.drop('target', axis=1)
y = data['target']

# Initialize SMOTE
smote = SMOTE(random_state=42)

# Perform SMOTE
X_resampled, y_resampled = smote.fit_resample(X, y)

# Print the new class distribution
print('Original dataset shape:', Counter(y))
print('Resampled dataset shape:', Counter(y_resampled))
