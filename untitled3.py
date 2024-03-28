result['Percentage'] = result.groupby('entry_db_journey_page')['Number'].apply(lambda x: x / x.sum())
