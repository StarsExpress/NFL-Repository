
def rename_pass_rush_columns(columns: list):
    renamed_cols = []
    for column in columns:
        split_text = column.split('_')
        renamed_col = ' '.join(text.capitalize() for text in split_text)

        if 'Team Name' in renamed_col:
            renamed_col = renamed_col.replace(' Name', '')

        if 'Wins' in renamed_col:
            renamed_col = renamed_col.replace('Pass Rush ', '')

        if 'Snap Counts Pass Rush' in renamed_col:
            renamed_col = renamed_col.replace('Snap Counts Pass Rush', 'PR Snaps')

        if 'Pass Rush Win Rate' in renamed_col:
            renamed_col = renamed_col.replace('Pass Rush Win Rate', 'Win Rate')

        renamed_cols.append(renamed_col.replace('True Pass Set', 'TPS'))
    return renamed_cols
