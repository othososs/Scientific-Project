# Supposons que 'df' est votre DataFrame
df['min_session_number'] = df.groupby('mk_id')['session_number'].transform('min')
df['Return_visitors'] = df.apply(lambda row: 'First visit' if row['session_number'] == row['min_session_number'] else 'Returning visitor', axis=1)
df = df.drop('min_session_number', axis=1)  # Supprimer la colonne temporaire
