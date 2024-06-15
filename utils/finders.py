from config import LOGOS_FOLDER_PATH
import os
import pandas as pd
from matplotlib.offsetbox import OffsetImage
import matplotlib.pyplot as plt


def find_median(series: pd.Series):
    series = series.dropna()  # Inplace is false to copy input series.
    series.sort_values(inplace=True)

    total = len(series)
    if total % 2 == 1:
        return series.iloc[total // 2]

    return round((series.iloc[(total - 1) // 2] + series.iloc[total // 2]) / 2, 1)


def find_logos(teams: set, zoom: float):
    teams_logos = dict()
    for team in teams:
        logo_path = os.path.join(LOGOS_FOLDER_PATH, f'{team}.png')
        teams_logos.update({team: OffsetImage(plt.imread(logo_path), zoom=zoom)})
    return teams_logos
