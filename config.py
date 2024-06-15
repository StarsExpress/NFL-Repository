"""All configurations."""
import os

NFL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER_PATH = os.path.join(NFL_BASE_PATH, 'data')

LOGOS_FOLDER_PATH = os.path.join(NFL_BASE_PATH, 'logos')

PLOTS_FOLDER_PATH = os.path.join(NFL_BASE_PATH, 'plots')


TEAMS = [
    "ARZ", "ATL", "BLT", "BUF", "CAR", "CHI", "CIN", "CLV",
    "DAL", "DEN", "DET", "GB", "HST", "IND", "JAX", "KC",
    "LA", "LAC", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS"
]
