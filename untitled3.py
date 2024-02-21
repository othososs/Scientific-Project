import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Supposons que vos données soient dans un DataFrame Pandas appelé 'data'
# Assurez-vous que les colonnes sont correctement nommées
# (vous pouvez adapter les noms de colonnes selon vos données)

# Exemple de données (remplacez cela par vos propres données)
data = pd.DataFrame({
    'Category': ['A', 'B', 'C'],
    'Médiane': [10, 15, 20],
    'Moyenne': [12, 18, 22],
    'Écart-type': [2, 3, 4],
    'Min': [8, 12, 18],
    'Max': [15, 22, 25]
})

# Reformater les données pour les adapter à un boxplot
data_melted = pd.melt(data, id_vars=['Category'], value_vars=['Médiane', 'Moyenne', 'Écart-type', 'Min', 'Max'])

# Créer un boxplot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.boxplot(x="variable", y="value", hue="Category", data=data_melted)

plt.title('Résumé statistique')
plt.show()
