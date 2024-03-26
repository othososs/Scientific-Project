def get_exit_page_counts(df, entry_page, return_type):
    filtered_df = df[(df['entry_page'] == entry_page) & (df['return'] == return_type)]
    exit_page_counts = filtered_df['exit_page'].value_counts()
    return exit_page_counts

# Deposit
df_exit_page_deposit_first = get_exit_page_counts(df, 'deposit', 'first')
df_exit_page_deposit_second = get_exit_page_counts(df, 'deposit', 'second')

# Saving
df_exit_page_saving_first = get_exit_page_counts(df, 'saving', 'first')
df_exit_page_saving_second = get_exit_page_counts(df, 'saving', 'second')
