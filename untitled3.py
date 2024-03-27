import pandas as pd

# Création du DataFrame initial
data = {'entry_db_journey_page': ['Saving account', 'Saving account', 'Saving account', 'Deposits', 'Deposits', 'Deposits', 'Deposits'],
        'exit_page': ['google.com', 'instagram.com', 'microsoft.com', 'google.com', 'instagram.com','microsoft.com','google.com'],
        'session_number': [2, 4, 2, 1, 6, 3 ,7],
        'returning_visitor': [1,0 ,0 ,1 ,0 ,1 ,0],
        "mk_id": [23231 ,23948 ,43212 ,45642 ,2143 ,43232 ,3436]}

df = pd.DataFrame(data)

# Calculer le nombre et le pourcentage des pages de sortie par type d'entrée
result = df.groupby(['entry_db_journey_page','exit_page']).size().reset_index(name='Number')
result['Percentage'] = result.groupby('entry_db_journey_page')['Number'].apply(lambda x: x / float(df['exit_page'].nunique()))

# Ajouter les données pour "All"
all_data = df.groupby('exit_page').size().reset_index(name='Number')
all_data['Percentage'] = all_data['Number'] / df['exit_page'].count()
all_data['entry_db_journey_page'] = "All"

result = pd.concat([result[['exit_page','Number','Percentage','entry_db_journey_page']], all_data[['exit_page','Number','Percentage','entry_db_journey_page']]])

print(result)
