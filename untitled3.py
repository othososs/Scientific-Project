import pandas as pd

# Supposons que votre DataFrame s'appelle df

# Charger les données depuis votre fichier CSV ou autre source
# df = pd.read_csv("votre_fichier.csv")

# Assurez-vous que les colonnes sont correctement typées, en particulier la colonne "date"
# df['date'] = pd.to_datetime(df['date'])

# Groupement par mk id
grouped_by_client = df.groupby('mk id')

# Parcourir chaque groupe (client)
for client_id, client_data in grouped_by_client:
    print(f"Analyse pour le client {client_id}:")
    
    # Analyse des destinations des visiteurs pour ce client
    exit_pages_count = client_data['exit pages'].value_counts()
    print("Destinations les plus populaires :")
    print(exit_pages_count.head())
    
    # Analyse des pages d'entrée des visiteurs pour ce client
    entry_pages_count = client_data['entry pages'].value_counts()
    print("\nPages d'entrée les plus populaires :")
    print(entry_pages_count.head())
    
    # Analyse des pages d'entrée du parcours client pour ce client
    entry_db_journey_count = client_data['entry db_journey page'].value_counts()
    print("\nPages d'entrée du parcours client les plus populaires :")
    print(entry_db_journey_count.head())
    
    # Analyse des retours des visiteurs pour ce client
    return_visits = client_data[client_data['session number'] > 1]
    return_visits_count = return_visits['entry pages'].value_counts()
    print("\nNombre de retours par page d'entrée pour ce client :")
    print(return_visits_count)
    print("\n----------------------\n")
