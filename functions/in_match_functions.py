import random
import pandas as pd

lines = pd.read_csv('sim_data\commentary.csv')

def match_data_collection(data, participants):
    # Retrieve all relevant sim_data from nation_df, player df

    nation_df, player_df = data[0], data[1]
    home, away = participants[0], participants[1]

    # home
    p_home = (float(nation_df.loc[nation_df['Country'] == home]['Attack'].iloc[0]) /
              float(nation_df.loc[nation_df['Country'] == away]['Defense'].iloc[0])) / 90
    # p_home = (float(nation_df.loc[nation_df['Country'] == home]['Attack']) / float(nation_df.loc[nation_df['Country'] == away]['Defense']))/90
    home_players = player_df.loc[player_df['Country'] == home]['Name'].tolist()
    home_atk = player_df.loc[player_df['Country'] == home]['Attack'].tolist()
    home_pass = player_df.loc[player_df['Country'] == home]['Passing'].tolist()

    # away
    p_away = (float(nation_df.loc[nation_df['Country'] == away]['Attack'].iloc[0]) /
              float(nation_df.loc[nation_df['Country'] == home]['Defense'].iloc[0])) / 90
    # p_away = (float(nation_df.loc[nation_df['Country'] == away]['Attack']) / float(nation_df.loc[nation_df['Country'] == home]['Defense']))/90 (Depreciated)
    away_players = player_df.loc[player_df['Country'] == away]['Name'].tolist()
    away_atk = player_df.loc[player_df['Country'] == away]['Attack'].tolist()
    away_pass = player_df.loc[player_df['Country'] == away]['Passing'].tolist()

    return p_home, home_players, home_atk, home_pass, p_away, away_players, away_atk, away_pass


def detailed_sim_goal(sim_info, minute, min_score, score, player_df, home, home_players, home_atk, home_pass, away, away_players, away_atk, away_pass,
                            WC, scorers, assisters):

    # Home goal
    if min_score[0] == 1:
        scorer = (random.choices(home_players, weights=home_atk, k=1))[0]
        index = home_players.index(scorer)
        player_df.loc[player_df['Name'] == scorer, 'Goals'] += 1
        if WC > 0:
            player_df.loc[player_df['Name'] == scorer, 'WC_Goals'] += 1
        scorers.append(scorer)

        x = random.uniform(0, 10)
        if x < 8:
            possible_assisters = home_players[:]
            possible_assisters.pop(index)
            possible_weights = home_pass[:]
            possible_weights.pop(index)
            assister = (random.choices(home_players, weights=home_pass, k=1))[0]
            player_df.loc[player_df['Name'] == assister, 'Assists'] += 1
            if WC > 0:
                player_df.loc[player_df['Name'] == assister, 'WC_Assists'] += 1
            assisters.append(assister)

    # Away goal
    if min_score[1] == 1:
        scorer = (random.choices(away_players, weights=away_atk, k=1))[0]
        index = away_players.index(scorer)
        player_df.loc[player_df['Name'] == scorer, 'Goals'] += 1
        if WC > 0:
            player_df.loc[player_df['Name'] == scorer, 'WC_Goals'] += 1
        scorers.append(scorer)

        x = random.uniform(0, 10)
        if x < 8:
            possible_assisters = away_players[:]
            possible_assisters.pop(index)
            possible_weights = away_pass[:]
            possible_weights.pop(index)
            assister = (random.choices(away_players, weights=away_pass, k=1))[0]
            player_df.loc[player_df['Name'] == assister, 'Assists'] += 1
            if WC > 0:
                player_df.loc[player_df['Name'] == assister, 'WC_Assists'] += 1
            assisters.append(assister)

    if sim_info[0] % 2 == 0:

        if sim_info[1] > 0:
            if sim_info[0] == 0:
                print(f"\nGoal {minute}, {scorer}, {score[0]} - {score[1]}")
                commentary('goal')
            else:
                print(f"\nGoal {minute + 90}, {scorer}, {score[0]} - {score[1]}")
                commentary('goal')
        else:
            if sim_info[0] == 0:
                print(f"\nGoal {minute}, {scorer}, {score[0]} - {score[1]}")
            else:
                print(f"\nGoal {minute + 90}, {scorer}, {score[0]} - {score[1]}")

    return player_df, scorers, assisters



def commentary(type):

    r, c = lines.shape
    n = random.randint(0, r - 1)
    line = lines.loc[n, type]
    print(line)

