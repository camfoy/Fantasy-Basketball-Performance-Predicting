import requests
from parsers.players_season_totals import parse_season_totals_for_players
from parsers.advanced_players_season_totals import parse_advanced_season_totals_for_players
from parsers.players_per_game_stats import parse_per_game_stats_for_players

BASE_URL = 'https://www.basketball-reference.com'

def players_season_totals(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'
    response = requests.get(url)
    response.raise_for_status()
    return parse_season_totals_for_players(response.content)

def players_advanced_season_totals(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'
    response = requests.get(url)
    response.raise_for_status()
    return parse_advanced_season_totals_for_players(response.content)

def players_per_game_stats(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_per_game.html'
    response = requests.get(url)
    response.raise_for_status()
    return parse_per_game_stats_for_players(response.content)