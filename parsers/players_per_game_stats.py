from lxml import html
from utilities import str_to_int, str_to_float
from helpers import TEAM_ABBREVIATIONS_TO_TEAM

def parse_player_per_game_stats(row):
    return {
        "name": str(row[1].text_content()),
        "position": str(row[2].text_content()),
        "age": str_to_int(row[3].text_content(), default=None),
        "team": TEAM_ABBREVIATIONS_TO_TEAM.get(row[4].text_content()),
        "games_played": str_to_int(row[5].text_content()),
        "games_started": str_to_int(row[6].text_content()),
        "minutes_played_per_game": str_to_float(row[7].text_content()),
        "field_goals_per_game": str_to_float(row[8].text_content()),
        "field_goal_attempts_per_game": str_to_float(row[9].text_content()),
        "field_goal_percentage": str_to_float(row[10].text_content()),
        "three_point_field_goals_per_game": str_to_float(row[11].text_content()),
        "three_point_field_goal_attempts_per_game": str_to_float(row[12].text_content()),
        "three_point_field_goal_percentage": str_to_float(row[13].text_content()),
        "two_point_field_goals_per_game": str_to_float(row[14].text_content()),
        "two_point_field_goal_attempts_per_game": str_to_float(row[15].text_content()),
        "two_point_field_goal_percentage": str_to_float(row[16].text_content()),
        "effective_field_goal_percentage": str_to_float(row[17].text_content()),
        "free_throws_per_game": str_to_float(row[18].text_content()),
        "free_throw_attempts_per_game": str_to_float(row[19].text_content()),
        "free_throw_percentage": str_to_float(row[20].text_content()),
        "offensive_rebounds_per_game": str_to_float(row[21].text_content()),
        "defensive_rebounds_per_game": str_to_float(row[22].text_content()),
        "total_rebounds_per_game": str_to_float(row[23].text_content()),
        "assists_per_game": str_to_float(row[24].text_content()),
        "steals_per_game": str_to_float(row[25].text_content()),
        "blocks_per_game": str_to_float(row[26].text_content()),
        "turnovers_per_game": str_to_float(row[27].text_content()),
        "personal_fouls_per_game": str_to_float(row[28].text_content()),
        "points_per_game": str_to_float(row[29].text_content()),
    }

def parse_per_game_stats_for_players(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="per_game_stats"]/tbody/tr[contains(@class, "full_table") or contains(@class, "italic_text partial_table") and not(contains(@class, "rowSum"))]')
    per_game = []
    for row in rows:
        if row[4].text_content() != "TOT":
            per_game.append(parse_player_per_game_stats(row))
    return per_game