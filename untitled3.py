import pandas as pd

# Supposons que votre DataFrame s'appelle df
# Je vais créer un exemple de DataFrame pour la démonstration
data = {
    'date': ['2024-03-01', '2024-03-01', '2024-03-02', '2024-03-02', '2024-03-03'],
    'entry_page': ['landing deposit page', 'product', 'landing deposit page', 'product', 'product'],
    'exit_page': ['product', 'checkout', 'checkout', 'landing deposit page', 'checkout'],
    'session_number': [1, 2, 1, 2, 1],  # Session number modifié
    'mk_id_visitors': [101, 102, 101, 103, 101]
}

df = pd.DataFrame(data)

# Sélectionner les visites où l'entrée est "landing deposit page"
landing_deposit_entries = df[df['entry_page'] == 'landing deposit page']

# Sélectionner les visites des mêmes visiteurs lorsqu'ils quittent
exit_pages = landing_deposit_entries.groupby('mk_id_visitors')['exit_page'].unique()

# Sélectionner les return visitors en filtrant par session number > 1
return_visits = df[df['mk_id_visitors'].isin(exit_pages.index) & (df['session_number'] > 1)]
return_entry_pages = return_visits.groupby('mk_id_visitors')['entry_page'].unique()

# Sélectionner la date de la première entrée pour chaque visiteur
first_entry_dates = landing_deposit_entries.groupby('mk_id_visitors')['date'].min()

# Sélectionner la date de retour pour chaque visiteur
return_dates = return_visits.groupby('mk_id_visitors')['date'].min()

# Afficher les résultats
print("Nombre de visiteurs qui sont entrés par 'landing deposit page':", len(landing_deposit_entries))
print("\nPages par lesquelles les mêmes visiteurs sont partis après avoir entré par 'landing deposit page':")
print(exit_pages)
print("\nPages par lesquelles les mêmes visiteurs sont revenus après avoir quitté par 'landing deposit page':")
print(return_entry_pages)
print("\nDate de la première entrée pour chaque visiteur:")
print(first_entry_dates)
print("\nDate de retour pour chaque visiteur:")
print(return_dates)
