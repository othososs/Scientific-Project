from imblearn.over_sampling import SMOTE
from collections import Counter

# Séparation des données
X = data.drop('target', axis=1)
y = data['target']

# Rapport désiré entre les classes minoritaire et majoritaire
# Par exemple, 0.5 signifie que le nombre d'instances de la classe minoritaire
# sera égal à la moitié du nombre d'instances de la classe majoritaire
desired_ratio = 0.5

# Initialisation de SMOTE avec le rapport désiré
smote = SMOTE(sampling_strategy=desired_ratio, random_state=42)

# Application de SMOTE
X_resampled, y_resampled = smote.fit_resample(X, y)

# Affichage de la nouvelle répartition des classes
print('Répartition des classes initiale :', Counter(y))
print('Répartition des classes après SMOTE :', Counter(y_resampled))
