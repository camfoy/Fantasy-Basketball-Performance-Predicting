import pandas as pd
import numpy as np
from helpers import players_season_totals_columns, advanced_players_season_totals_columns


def single_season_cleaner(df, dummy_columns, players_season_totals_columns=players_season_totals_columns, advanced_players_season_totals_columns=advanced_players_season_totals_columns):

    if dummy_columns:
        df = pd.get_dummies(df, columns=dummy_columns)

    for option in ['position', 'team']:
        if option in df.columns:
            answer = input(f'Would you like to create a "{option.capitalize()}" model? (y/n): ')
            if answer.lower() == 'y' or answer.lower() == 'yes':
                answer = input(f'Input the {option} you would like a model for: ')
                df = df.loc[df[option]==answer.upper()]
                df = df.drop(columns=[option])
            else:
                df = df.drop(columns=[option])

    subset_columns = ['season_end_year', 'name']

    dupe_df = df.loc[df.duplicated(subset=subset_columns, keep=False)]
    df = df.drop(index=dupe_df.index.to_list())

    subset_columns.extend(['age'])

    advanced_players_season_totals_columns = [x for x in advanced_players_season_totals_columns if x not in players_season_totals_columns]
    advanced_players_season_totals_columns.extend([x for x in players_season_totals_columns if 'percentage' in x])
    weighted_average_columns = advanced_players_season_totals_columns

    sum_columns = [x for x in dupe_df.columns.tolist() if x not in subset_columns and x not in weighted_average_columns]

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
                    try:
                        numerator = 0
                        for i in range(0, number_of_teams):
                            numerator += player_season_df[x].iloc[i]*player_season_df['games_played'].iloc[i]
                        player_dict.update({x:numerator/games_played_total})
                    except KeyError:
                        pass
                df = df.append(player_dict, ignore_index=True)

    return df.sort_values(by=subset_columns).reset_index(drop=True)


def normalize_games_played(df, players_season_totals_columns=players_season_totals_columns, advanced_players_season_totals_columns=advanced_players_season_totals_columns):

    answer = input('Would you like to drop all seasons containing under a certain amount of games played? (y/n): ')
    if answer == 'y' or answer.lower() == 'yes':
        min_games = int(input("What's the minimum number of games played desired? (enter a number): "))
        index_list = df[df['games_played']<min_games].index.tolist()
        df = df.drop(index_list, axis=0)

    answer = input('Would you like to normalize games played? (y/n) : ')
    if answer == 'y' or answer.lower() == 'yes':
        static_columns = ['name', 'position', 'age', 'team', 'season_end_year']
        static_columns = static_columns + [x for x in players_season_totals_columns if 'percentage' in x]

        moving_columns = [x for x in players_season_totals_columns if x not in static_columns]
        moving_columns = moving_columns + ['offensive_win_shares', 'defensive_win_shares', 'win_shares']

        for x in moving_columns:
            df[x] = df[x]/df['games_played'] * 82

    return df.drop(columns=['games_played'])


def get_independent_variables_and_finalize(df):

    df['future_fantasy_points'] = np.nan

    for player in df['name'].unique():
        year_list = df.loc[df['name']==player]['season_end_year'].tolist()

        for year in year_list:
            try:
                df.loc[(df['name']==player) & (df['season_end_year']==year), 'future_fantasy_points'] = df.loc[(df['name']==player) & (df['season_end_year']==year+1)]['fantasy_points'].iloc[0]
            except IndexError:
                pass

    return df.dropna().drop(columns=['name', 'season_end_year'])