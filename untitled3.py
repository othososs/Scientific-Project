
# Pour la première partie (visiteurs 'First Visit')
first_visits = df[(df['returning_visitor'].str.lower() == 'first visit') & df['entry_db_journey_page'].isin(['Deposits', 'Saving account'])]

first_visits_grouped = first_visits.groupby(['entry_db_journey_page', 'exit_page']).size().reset_index(name='Number_of_visitors')
print("Première partie :\n", first_visits_grouped)

# Pour la deuxième partie (visiteurs 'Returning visitor')
# Obtenez les mk_id des visiteurs 'First Visit'
first_visit_mk_ids = first_visits['mk_id'].unique()

# Filtrer les visites ultérieures de ces visiteurs
returning_visits = df[df['mk_id'].isin(first_visit_mk_ids) & (df['returning_visitor'].str.lower() == 'returning visitor')]

returning_visits_grouped = returning_visits.groupby(['entry_db_journey_page', 'exit_page']).size().reset_index(name='Number_of_visitors')
print("Deuxième partie :\n", returning_visits_grouped)
