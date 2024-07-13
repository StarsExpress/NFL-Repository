import os
import pandas as pd
from config import DATA_FOLDER_PATH


original_pass_rush_path = os.path.join(
        DATA_FOLDER_PATH, f"2023 NFL Front 7 Pass Rush.xlsx"
)
original_pass_rush_df = pd.read_excel(
        original_pass_rush_path, sheet_name=["DI", "ED"]
)
original_pass_rush_df = pd.concat([original_pass_rush_df["DI"], original_pass_rush_df["ED"]], axis=0)


def compute_pass_rush_rank(
        metric: str,
        rate_name: str,
        position: str = None,
        teams: list = None,
        return_rank_df: bool = False
):

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
    pass_rush_df[f"{rate_name} Rank"] = pass_rush_df[f"{rate_name}"].rank(
        method="min", ascending=False
    )

    pass_rush_df[f"TPS {rate_name}"] = pass_rush_df[f"TPS {metric}"] / pass_rush_df["TPS PR Opp"]
    pass_rush_df[f"TPS {rate_name}"] *= 100
    pass_rush_df[f"TPS {rate_name}"] = pass_rush_df[f"TPS {rate_name}"].round(2)
    pass_rush_df[f"TPS {rate_name} Rank"] = pass_rush_df[f"TPS {rate_name}"].rank(
        method="min", ascending=False
    )

    pass_rush_df.sort_values(by=f"{rate_name} Rank", ascending=True, inplace=True)
    cols = [f"{rate_name} Rank", "Team", f"{rate_name}", f"{metric}", "PR Opp"]

    rank_df = pass_rush_df[["Team", f"{rate_name} Rank"]]
    if teams is None:
        if return_rank_df is False:
            print(pass_rush_df[cols].to_markdown(tablefmt="grid", index=False), '\n')

    else:
        if return_rank_df is False:
            print(pass_rush_df[pass_rush_df['Team'].isin(teams)][cols].to_markdown(tablefmt="grid", index=False), '\n')
        rank_df = rank_df[rank_df['Team'].isin(teams)]

    pass_rush_df.sort_values(by=f"TPS {rate_name} Rank", ascending=True, inplace=True)
    tps_cols = [f"TPS {rate_name} Rank", "Team", f"TPS {rate_name}", f"TPS {metric}", "TPS PR Opp"]

    rank_df = rank_df.merge(pass_rush_df[["Team", f"TPS {rate_name} Rank"]],
                            left_on="Team", right_on="Team", how="inner")
    if teams is None:
        if return_rank_df is False:
            print(pass_rush_df[tps_cols].to_markdown(tablefmt="grid", index=False), '\n')

    else:
        if return_rank_df is False:
            print(
                pass_rush_df[pass_rush_df['Team'].isin(teams)][tps_cols].to_markdown(tablefmt="grid", index=False), '\n'
            )

    if return_rank_df:
        return rank_df


if __name__ == "__main__":
    query_teams = ['PIT', 'GB', 'KC']
    compute_pass_rush_rank('Wins', 'Win Rate', teams=query_teams)
    compute_pass_rush_rank('Pressures', 'Pressure Rate', teams=query_teams)
    compute_pass_rush_rank('Havoc', 'Havoc Rate', teams=query_teams)
