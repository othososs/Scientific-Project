# Importer pandas
import pandas as pd

# Calculer le nombre total de sorties pour chaque type d'entrée de page
total_exit_counts = df['exit_page'].value_counts()

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
return_visitors = create_dataset(['deposit', 'saving'], 'return')
first_visitors = create_dataset(['deposit', 'saving'], 'first')
all_visitors = create_dataset(['deposit', 'saving'], ['first', 'second'])
