    aligned_exit_page_counts, aligned_total_exit_counts = exit_page_counts.align(total_exit_counts, fill_value=0)
    percentage = aligned_exit_page_counts / aligned_total_exit_counts
