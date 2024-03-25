import pandas as pd
import matplotlib.pyplot as plt

# Supposons que votre DataFrame s'appelle df

# Charger les données depuis votre fichier CSV ou autre source
# df = pd.read_csv("votre_fichier.csv")

# Assurez-vous que les colonnes sont correctement typées, en particulier la colonne "date"
# df['date'] = pd.to_datetime(df['date'])

# Analyse des destinations des visiteurs
exit_pages_count = df['exit pages'].value_counts()

# Affichage des destinations les plus populaires
print("Destinations les plus populaires :")
print(exit_pages_count.head())

# Analyse des pages d'entrée des visiteurs
entry_pages_count = df['entry pages'].value_counts()

# Affichage des pages d'entrée les plus populaires
print("\nPages d'entrée les plus populaires :")
print(entry_pages_count.head())

# Analyse des pages d'entrée du parcours client
entry_db_journey_count = df['entry db_journey page'].value_counts()

# Affichage des pages d'entrée du parcours client les plus populaires
print("\nPages d'entrée du parcours client les plus populaires :")
print(entry_db_journey_count.head())

# Analyse des retours des visiteurs
return_visits = df[df['session number'] > 1]

# Calcul du nombre de retours par page d'entrée
return_visits_count = return_visits['entry pages'].value_counts()

# Affichage des pages d'entrée avec le nombre de retours
print("\nNombre de retours par page d'entrée :")
print(return_visits_count)

# Visualisation des données
plt.figure(figsize=(10, 6))
entry_pages_count.plot(kind='bar', color='blue', alpha=0.7)
plt.title('Pages d\'entrée les plus populaires')
plt.xlabel('Page')
plt.ylabel('Nombre de visites')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
