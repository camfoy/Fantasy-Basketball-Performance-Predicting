import pandas as pd
from collectors import get_merged_data

def pre_modeling_modifier(year_list, dummy_columns):
    df = get_merged_data(year_list=year_list)
    df = pd.get_dummies(df, columns=dummy_columns)
    subset_columns = [x for x in ['name', 'season_end_year', 'position', 'team'] if x not in dummy_columns]
    dupe_df = df[df.duplicated(subset=subset_columns, keep=False)]
    df = df.drop(index=dupe_df.index.to_list())
    sum_columns = ['games_played', 'games_started', 'fantasy_points']
    weighted_average_columns = [x for x in dupe_df.columns if x not in subset_columns and x not in sum_columns]
    for player in dupe_df['name'].unique():
        for season in dupe_df['season_end_year'].unique():
            player_season_df = dupe_df.loc[(dupe_df['name']==player) & (dupe_df['season_end_year']==season)]
            if not player_season_df.empty:
                number_of_teams = len(player_season_df)
                games_played_total = player_season_df['games_played'].sum()
                player_dict = {}
                for x in subset_columns:
                    player_dict.update({x:player_season_df[x].iloc[0]})
                for x in sum_columns:
                    player_dict.update({x:player_season_df[x].sum()})
                for x in weighted_average_columns:
                    numerator = 0
                    for i in range(0, number_of_teams):
                        numerator += player_season_df[x].iloc[i]*player_season_df['games_played'].iloc[i]
                    player_dict.update({x:numerator/games_played_total})
                df = df.append(player_dict, ignore_index=True)
    average_columns = weighted_average_columns
    return df.sort_values(by=['season_end_year', 'name']), subset_columns, sum_columns, average_columns