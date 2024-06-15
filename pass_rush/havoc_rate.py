from config import DATA_FOLDER_PATH, PLOTS_FOLDER_PATH
from utils.finders import find_median, find_logos
import os
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnnotationBbox
import matplotlib.pyplot as plt


position_names = {'DI': 'Defensive Interior', 'ED': 'Edge', 'LB': 'Linebacker'}
logo_boxes = find_logos(0.004)

x_axis_dict = {'metric': 'TPS Havoc Rate'}
x_axis_dict.update({'col': f"{x_axis_dict['metric']}",
                    'label': f"PFF {x_axis_dict['metric']} (%)"})

y_axis_dict = {'metric': 'Havoc Rate'}
y_axis_dict.update({'col': f"{y_axis_dict['metric']}",
                    'label': f"PFF {y_axis_dict['metric']} (%)"})

required_cols = ['Player', 'Team', x_axis_dict['col'], y_axis_dict['col']]
name_size = 4
plt.figure(figsize=(10, 10))


def plot_havoc_rate(season: int, position: str, snaps_threshold: int):
    pass_rush_path = os.path.join(DATA_FOLDER_PATH, f'{season} NFL Front 7 Pass Rush.xlsx')
    pass_rush_df_dict = pd.read_excel(pass_rush_path, sheet_name=None)

    if position not in position_names.keys():
        raise ValueError('Invalid position. Choose from DI, ED, or LB.')

    pass_rush_df = pass_rush_df_dict[position].dropna()
    pass_rush_df = pass_rush_df[pass_rush_df['PR Snaps'] >= snaps_threshold][required_cols]
    if len(pass_rush_df) <= 0:
        return

    # Use white dots to prevent blocking team logos.
    sns.scatterplot(data=pass_rush_df, x=x_axis_dict['col'],
                    y=y_axis_dict['col'], s=100, color='white')

    for _, row in pass_rush_df.iterrows():  # Logo & name annotations.
        x_value, y_value = row[x_axis_dict['col']], row[y_axis_dict['col']]

        logo_box = AnnotationBbox(logo_boxes[row['Team']], (x_value, y_value),
                                  frameon=False, box_alignment=(0.5, 0.5))
        plt.gca().add_artist(logo_box)

        plt.text(  # Ensure text is a bit righter from logo.
            x=1.025 * x_value, y=y_value, s=row['Player'],
            fontdict=dict(color='black', size=name_size, ha='left', va='center')
        )

    title = f"{season} NFL {position_names[position]} Havoc Rate"
    plt.title(title, fontsize=14, pad=40)

    note = f"players with at least {snaps_threshold} pass rush snaps. Source: PFF."
    note += 'Havoc Rate = (Sacks + Hits) / Pass Rush Snaps.'
    plt.text(x=0.5, y=1.05, s=f'Note: {len(pass_rush_df)} {note}', fontsize=10,  # Add number of players in notes.
             ha='center', va='top', transform=plt.gca().transAxes)

    plt.xlabel(x_axis_dict['label'])
    plt.xticks(range(0, int(pass_rush_df[x_axis_dict['col']].max()) + 1, 2))

    plt.ylabel(y_axis_dict['label'])
    plt.yticks(range(0, int(pass_rush_df[y_axis_dict['col']].max()) + 1, 2))

    x_median = find_median(pass_rush_df[x_axis_dict['col']])
    plt.axvline(x=x_median, color='gray', linestyle='--')
    plt.text(x_median, plt.ylim()[0], f'Median: {x_median}',
             color='black', ha='left', va='bottom')

    y_median = find_median(pass_rush_df[y_axis_dict['col']])
    plt.axhline(y=y_median, color='gray', linestyle='--')
    plt.text(plt.xlim()[0], y_median, f'Median: {y_median}',
             color='black', ha='left', va='bottom')

    plot_path = os.path.join(PLOTS_FOLDER_PATH, f'{season} {position} Havoc Rate.jpeg')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close('all')


if __name__ == "__main__":
    plot_havoc_rate(2023, 'DI', 170)
