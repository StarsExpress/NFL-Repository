from config import DATA_FOLDER_PATH, OUTPUTS_FOLDER_PATH, FRONT_7_NAMES
from utils.finders import find_median, find_logos
import os
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnnotationBbox
import matplotlib.pyplot as plt


logo_boxes = find_logos(0.004)
name_size = 4
plt.figure(figsize=(10, 10))


def plot_metrics(season: int, position: str, snaps_threshold: int,
                 x_metric: str, y_metric: str, x_rate: bool = True, y_rate: bool = True,
                 use_tps: bool = True, extra_note: str = ''):
    if position not in FRONT_7_NAMES.keys():
        raise ValueError('Invalid position. Choose from DI, ED, or LB.')

    pass_rush_path = os.path.join(DATA_FOLDER_PATH, f'{season} NFL Front 7 Pass Rush.xlsx')
    pass_rush_df_dict = pd.read_excel(pass_rush_path, sheet_name=None)

    pass_rush_df = pass_rush_df_dict[position].dropna()
    pass_rush_df = pass_rush_df[pass_rush_df['PR Snaps'] >= snaps_threshold]
    if len(pass_rush_df) <= 0:
        return

    tps_suffix = 'TPS ' if use_tps else ''
    x_axis_dict = {'metric': f'{tps_suffix}{x_metric}'}
    x_label_suffix = ' (%)' if x_rate else ''
    x_axis_dict.update({'col': f"{x_axis_dict['metric']}",
                        'label': f"PFF {x_axis_dict['metric']}{x_label_suffix}"})

    y_axis_dict = {'metric': f'{tps_suffix}{y_metric}'}
    y_label_suffix = ' (%)' if y_rate else ''
    y_axis_dict.update({'col': f"{y_axis_dict['metric']}",
                        'label': f"PFF {y_axis_dict['metric']}{y_label_suffix}"})

    # White dots prevent blocking team logos.
    sns.scatterplot(data=pass_rush_df, x=x_axis_dict['col'],
                    y=y_axis_dict['col'], s=100, color='white')

    for _, row in pass_rush_df.iterrows():  # Logo & name annotations.
        x_value, y_value = row[x_axis_dict['col']], row[y_axis_dict['col']]
        logo_box = AnnotationBbox(logo_boxes[row['Team']], (x_value, y_value),
                                  frameon=False, box_alignment=(0.5, 0.5))
        plt.gca().add_artist(logo_box)

        plt.text(
            x=1.025 * x_value, y=y_value, s=row['Player'],
            fontdict=dict(color='black', size=name_size, ha='left', va='center')
        )  # Ensure text is a bit righter from logo.

    title = f"{season} NFL {FRONT_7_NAMES[position]} {tps_suffix}Pass Rush {x_metric} & {y_metric}"
    plt.title(title, fontsize=14, pad=40)

    note = f"players with at least {snaps_threshold} pass rush snaps. Source: PFF."
    if len(extra_note) > 0:
        note += f'\n{extra_note}'

    plt.text(x=0.5, y=1.05, s=f'Note: {len(pass_rush_df)} {note}', fontsize=10,
             ha='center', va='top', transform=plt.gca().transAxes)

    plt.xlabel(x_axis_dict['label'])
    plt.ylabel(y_axis_dict['label'])

    x_median = find_median(pass_rush_df[x_axis_dict['col']])
    plt.axvline(x=x_median, color='gray', linestyle='--')
    plt.text(x_median, plt.ylim()[0], f'Median: {x_median}',
             color='black', ha='left', va='bottom')

    y_median = find_median(pass_rush_df[y_axis_dict['col']])
    plt.axhline(y=y_median, color='gray', linestyle='--')
    plt.text(plt.xlim()[0], y_median, f'Median: {y_median}',
             color='black', ha='left', va='bottom')

    plot_path = os.path.join(OUTPUTS_FOLDER_PATH, f'{season}',
                             f'{position} {tps_suffix}{x_metric} V.S {y_metric}.jpeg')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close('all')


if __name__ == "__main__":
    from config import HAVOC_NOTE
    plot_metrics(2023, 'DI', 170,
                 'Win Rate', 'Havoc Rate', extra_note=HAVOC_NOTE)
