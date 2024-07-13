import pandas as pd
from pass_rush_rank import compute_pass_rush_rank


if __name__ == '__main__':
    query_teams = None
    query_position = None
    all_rank_df = pd.DataFrame()
    metrics = [("Wins", "Win Rate"), ("Pressures", "Pressure Rate"), ("Havoc", "Havoc Rate")]

    for idx, metric in enumerate(metrics):
        if idx == 0:
            all_rank_df = compute_pass_rush_rank(
                metric[0], metric[1], teams=query_teams, position=query_position, return_rank_df=True
            )
            continue

        rank_df = compute_pass_rush_rank(
            metric[0], metric[1], teams=query_teams, position=query_position, return_rank_df=True
        )
        all_rank_df = all_rank_df.merge(rank_df, left_on="Team", right_on="Team", how="inner")

    all_rank_df.set_index('Team', inplace=True)
    all_rank_df['Metrics Avg Rank'] = all_rank_df.mean(axis=1).round(2)
    all_rank_df.sort_values(by=['Metrics Avg Rank'], ascending=True, inplace=True)
    all_rank_df.reset_index(inplace=True)
    all_rank_df.insert(0, 'Pass Rush Rank', all_rank_df['Metrics Avg Rank'].rank(method="min", ascending=True))
    print(all_rank_df[['Pass Rush Rank', 'Team', 'Metrics Avg Rank']].to_markdown(tablefmt="grid", index=False))
