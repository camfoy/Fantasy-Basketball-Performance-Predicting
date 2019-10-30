import pandas as pd
import datetime
from client import players_season_totals, players_advanced_season_totals, players_per_game_stats

def get_merged_data(year_list):

    totals_df = get_players_season_totals(year_list=year_list)
    advanced_df = get_players_advanced_season_totals(year_list=year_list)
    per_game_df = get_players_per_game_stats(year_list=year_list)
    interim_df = per_game_df.merge(totals_df[['name', 'position', 'age', 'team', 'games_played', 'games_started', 'fantasy_points']], how='inner')
    master_df = interim_df.merge(advanced_df.drop(columns=['minutes_played']), how='inner')
    # first_year = year_list[0]
    # last_year = year_list[-1]

    # return master_df.to_csv(f"C:\\Users\\CA015FO\\basketball\\data\\basketball_reference_data_{first_year}_{last_year}", index=False)
    return master_df

def get_players_season_totals(year_list):

    df = pd.DataFrame()
    for i in year_list:
        data = players_season_totals(season_end_year=i)
        data = pd.DataFrame(data)
        data['season_end_year'] = i
        df = df.append(data, ignore_index=True)
    
    df['fantasy_points'] = (
        df['attempted_field_goals']*(-0.45) + 
        df['made_field_goals']*(1) + 
        df['attempted_free_throws']*(-0.75) + 
        df['made_free_throws']*(1) + 
        df['made_three_point_field_goals']*(3) + 
        df['points']*(0.5) + 
        (df['offensive_rebounds'] + df['defensive_rebounds'])*(1.5) + 
        df['assists']*(2) + 
        df['steals']*(3) + 
        df['blocks']*(3) +
        df['turnovers']*(-2)
    )

    return df

def get_players_advanced_season_totals(year_list):

    df = pd.DataFrame()
    for i in year_list:
        data = players_advanced_season_totals(season_end_year=i)
        data = pd.DataFrame(data)
        data['season_end_year'] = i
        df = df.append(data, ignore_index=True)

    return df

def get_players_per_game_stats(year_list):

    df = pd.DataFrame()
    for i in year_list:
        data = players_per_game_stats(season_end_year=i)
        data = pd.DataFrame(data)
        data['season_end_year'] = i
        df = df.append(data, ignore_index=True)

    return df