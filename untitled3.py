def get_exit_page_counts(df, entry_pages, return_type):
    filtered_df = df[(df['entry_page'].isin(entry_pages)) & (df['return'] == return_type)]
    exit_page_counts = filtered_df['exit_page'].value_counts()
    return exit_page_counts

# Deposit
df_exit_page_deposit_first = get_exit_page_counts(df, ['deposit'], 'first')
df_exit_page_deposit_second = get_exit_page_counts(df, ['deposit'], 'second')

# Saving
df_exit_page_saving_first = get_exit_page_counts(df, ['saving'], 'first')
df_exit_page_saving_second = get_exit_page_counts(df, ['saving'], 'second')

# All (Deposit and Saving)
df_exit_page_all_first = get_exit_page_counts(df, ['deposit', 'saving'], 'first')
df_exit_page_all_second = get_exit_page_counts(df, ['deposit', 'saving'], 'second')
