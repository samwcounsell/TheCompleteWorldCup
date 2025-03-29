import pandas as pd
from scipy.stats import bernoulli
from functions.match_day_functions import match_data_collection, detailed_sim_goal, commentary
from functions. worldcup_functions_old import stadium_info
import time, os, json


# single_sim_match runs the whole match as part of a detailed World Cup simulations
def detailed_binomial_match(data, participants, WC, settings, stage, leg, ET):
    # run match_data_retrieval here
    # import not required
    # return p_home, p_away, player_lists and their ratings

    nation_df, player_df = data[0], data[1]
    home, away = participants[0], participants[1]

    scorers = []
    assisters = []

    # TODO: Add proper match introduction

    p_home, home_players, home_atk, home_pass, p_away, away_players, away_atk, away_pass = match_data_collection(
        data, participants)

    # Running binomial simulation with size 90
    #if WC > 0:
    #    stadium_info()

    if ET == 0:

        if stage == 'K':
            print(f"\n{home} v {away} (Leg {leg + 1}) :")
        else:
            print(f"\n{home} v {away}:")

        score_home, score_away = 0, 0

        for m in range(90):
            time.sleep(settings.delay)
            min_score = [bernoulli.rvs(p_home, size=1), bernoulli.rvs(p_away, size=1)]
            score_home, score_away = score_home + min_score[0], score_away + min_score[1]
            if sum(min_score) > 0:
                player_df, scorers, assisters = detailed_sim_goal(settings, m, min_score, [score_home, score_away], data[1], home, home_players, home_atk, home_pass, away, away_players, away_atk, away_pass,
                            WC, ET, scorers, assisters)

    # For knockout matches ET
    if ET == 1:

        print("ET Kick Off: ")

        score_home, score_away = 0, 0

        for m in range(30):
            time.sleep(settings.delay)
            min_score = [bernoulli.rvs(p_home, size=1), bernoulli.rvs(p_away, size=1)]
            score_home, score_away = score_home + min_score[0], score_away + min_score[1]
            if sum(min_score) > 0:
                player_df, scorers, assisters = detailed_sim_goal(settings, m, min_score, [score_home, score_away], data[1], home, home_players, home_atk, home_pass, away, away_players, away_atk, away_pass,
                            WC, ET, scorers, assisters)

    # Calculate scorers and assisters
    detailed_sim_nation_events(nation_df, home, away, score_home, score_away, WC)
    detailed_sim_player_events(player_df, home, away, WC)

    data = [nation_df, player_df]
    score = [score_home[0], score_away[0]]

    # TODO: Create df with columns,
    df = pd.DataFrame([[home, score_home[0]], [away, score_away[0]]], columns=['Country', 'Score'])

    # TODO: Store teams, score and scorers / assisters in df and save as json in same way as done for groups
    path = os.getcwd()
    file_path = os.path.join(path, f'app_data/matches_sim{settings.run_number}.json')

    with open(file_path, 'a') as f:
        # Convert the DataFrame to a JSON string
        json_df = df.to_json()

        # Create a dictionary with the identifier as the key and the JSON string as the value
        json_dict = {'id': f'{settings.confederation}{settings.stage}{home}{away}', 'data': json_df}

        # Convert the dictionary to a JSON string and write it to the file
        f.write(json.dumps(json_dict) + '\n')

    return data, score


def detailed_sim_nation_events(nation_df, home, away, score_home, score_away, WC):
    # Updating the nation sim_data after the game

    nation_df.loc[nation_df['Country'].isin([home, away]), 'P'] += 1

    # home
    nation_df.loc[nation_df['Country'] == home, 'GF'] += score_home
    nation_df.loc[nation_df['Country'] == home, 'GA'] += score_away
    if away == 0:
        nation_df.loc[nation_df['Country'] == home, 'CS'] += 1

    if WC > 0:
        # TODO: Split these back into individual lines so it works, try later to combine back into one line
        nation_df.loc[nation_df['Country'] == home, ['WC_P', 'WC_GF', 'WC_GA']] += [1, score_home, score_away]
        if away == 0:
            nation_df.loc[nation_df['Country'] == home, 'WC_CS'] += 1

    # away
    nation_df.loc[nation_df['Country'] == away, 'GF'] += score_away
    nation_df.loc[nation_df['Country'] == away, 'GA'] += score_home
    if home == 0:
        nation_df.loc[nation_df['Country'] == away, 'CS'] += 1

    if WC > 0:
        nation_df.loc[nation_df['Country'] == away, ['WC_P', 'WC_GF', 'WC_GA']] += [1, score_home, score_away]
        if home == 0:
            nation_df.loc[nation_df['Country'] == away, 'WC_CS'] += 1


# Calculates detail of main player events i.e., goals for a multi_sim_match
def detailed_sim_player_events(player_df, home, away, WC):

    player_df.loc[player_df['Country'] == home, 'P'] += 1
    if WC > 0:
        player_df.loc[player_df['Country'] == home, 'WC_P'] += 1

    player_df.loc[player_df['Country'] == away, 'P'] += 1
    if WC > 0:
        player_df.loc[player_df['Country'] == away, 'WC_P'] += 1