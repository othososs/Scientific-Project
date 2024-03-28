result['Percentage'] = result.groupby('entry_db_journey_page')['Number'].apply(lambda x: x / float(df[df['entry_db_journey_page'] == x.name]['exit_page'].nunique()))
