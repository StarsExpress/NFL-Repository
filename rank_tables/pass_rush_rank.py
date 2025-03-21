import os
import pandas as pd
from config import DATA_FOLDER_PATH


original_pass_rush_path = os.path.join(
    DATA_FOLDER_PATH, f"2024 NFL Front 7 Pass Rush.xlsx"
)
original_pass_rush_df = pd.read_excel(
    original_pass_rush_path, sheet_name=["DI", "ED"]
)
original_pass_rush_df = pd.concat(
    [original_pass_rush_df["DI"], original_pass_rush_df["ED"]], axis=0
)


def compute_pass_rush_rank(
    metric: str,
    rate_name: str,
    position: str = None,
    teams: list = None,
    return_rank_df: bool = False
) -> pd.DataFrame | None:

    if position is not None:
        pass_rush_df = original_pass_rush_df[original_pass_rush_df["Position"] == position]

    else:
        pass_rush_df = original_pass_rush_df.copy()

    groupby_cols = ["PR Opp", metric, "TPS PR Opp", f"TPS {metric}"]

    pass_rush_df = pass_rush_df.groupby(by=["Team"], as_index=False, sort=False)[
        groupby_cols
    ].sum()

    pass_rush_df[f"{rate_name}"] = pass_rush_df[metric] / pass_rush_df["PR Opp"]
    pass_rush_df[f"{rate_name}"] *= 100
    pass_rush_df[f"{rate_name}"] = pass_rush_df[f"{rate_name}"].round(2)
    pass_rush_df.insert(
        0, f"{rate_name} Rank", pass_rush_df[f"{rate_name}"].rank(method="min", ascending=False)
    )

    pass_rush_df.sort_values(by=f"{rate_name} Rank", ascending=True, inplace=True)
    if teams is not None:
        pass_rush_df = pass_rush_df[pass_rush_df['Team'].isin(teams)]

    cols = [f"{rate_name} Rank", "Team", f"{rate_name}", f"{metric}", "PR Opp"]
    if return_rank_df:
        return pass_rush_df[cols]
    print(pass_rush_df[cols].to_markdown(tablefmt="grid", index=False), '\n')

if __name__ == "__main__":
    query_teams = None
    compute_pass_rush_rank('Wins', 'Win Rate', teams=query_teams)
    compute_pass_rush_rank('Pressures', 'Pressure Rate', teams=query_teams)
    compute_pass_rush_rank('Havoc', 'Havoc Rate', teams=query_teams)
