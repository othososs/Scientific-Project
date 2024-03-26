import pandas as pd

# Supposons que df est le DataFrame avec lequel vous travaillez
# df = pd.read_csv('votre_data.csv')

# Calculer le nombre total de sorties pour chaque type de page d'entrée
total_exit_counts = df['exit_page'].value_counts()

# Définir une fonction pour obtenir les comptes de page de sortie
def get_exit_page_counts(df, entry_pages, return_type):
    # Filtrer le DataFrame en fonction des pages d'entrée et du type de retour
    filtered_df = df[df['entry_page'].isin(entry_pages) & df['return_type'].isin(return_type)]
    # Calculer les comptes de page de sortie
    exit_page_counts = filtered_df['exit_page'].value_counts()
    return exit_page_counts

# Définir une fonction pour créer chaque dataset
def create_dataset(entry_pages, return_type):
    exit_page_counts = get_exit_page_counts(df, entry_pages, return_type)
    percentage = exit_page_counts / total_exit_counts
    dataset = pd.DataFrame({
        'Exit_page_name': exit_page_counts.index,
        'Number_of_exit': exit_page_counts.values,
        'Percentage': percentage.values,
        'Type_of_entry_page': ', '.join(entry_pages)
    })
    return dataset

# Créer les datasets
return_visitors = create_dataset(['deposit', 'saving'], ['return'])
first_visitors = create_dataset(['deposit', 'saving'], ['first'])
all_visitors = create_dataset(['deposit', 'saving'], ['first', 'return'])

# Imprimer les datasets
print("Visiteurs de retour:\\n", return_visitors)
print("\\nVisiteurs pour la première fois:\\n", first_visitors)
print("\\nTous les visiteurs:\\n", all_visitors)
