import pandas as pd
import random
import time

example_teams = ['USA', 'Mexico', 'Canada', 'Iraq', 'Saudi Arabia', 'Iran', 'Uzbekistan', 'Japan', 'South Korea', 'Bahrain', 'UAE', 'Algeria', 'Nigeria', 'Senegal', 'Mali', 'Cameroon', 'Ghana', 'Tunisia', 'Madagascar', 'Gabon', 'Jamaica', 'El Salvador', 'Costa Rica', 'Brazil', 'Uruguay', 'Colombia', 'Argentina', 'Ecuador', 'Chile', 'New Zealand', 'Italy', 'England', 'Germany', 'Portugal', 'Czechia', 'Bulgaria', 'France', 'Belgium', 'Poland', 'Spain', 'Netherlands', 'North Macedonia', 'Sweden', 'Switzerland', 'Denmark', 'Austria', 'Curacao', 'Jordan']

def world_cup_draw(teams, settings, group_number, group_size):
    
    #TODO: Ask user to set delay for the draw
    #settings.delay = input(...)
    settings.delay = 0 # to be removed when input line added

    all_nations = pd.read_csv('data/nation_data.csv', usecols = ['Country', 'World Rank', 'Confederation'])
    nations = all_nations[all_nations['Country'].isin(teams)]
    nations = nations.sort_values('World Rank')

    # Ensuring Mexico, Canada and USA get drawn in A,B,D respectively
    teams = nations['Country'].tolist()
    teams = [x for x in teams if x not in ['USA', 'Mexico', 'Canada']]
    teams.insert(0, 'Mexico')
    teams.insert(1, 'Canada')
    teams.insert(3, 'USA')

    group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I",
                   "Group J", "Group K", "Group L"]

    # groups[i] will become groups_df[i].Country
    groups = group_names

    # Re-dataframing and sorting by teams to get confederations to ensure valid teams in same group
    nations = all_nations[all_nations['Country'].isin(teams)]
    nations = nations.set_index('Country')
    nations = nations.reindex(teams)
    nations = nations.reset_index(drop = False)

    for i in range(group_number):
        groups[i] = nations.iloc[i: i + 1]
            
    # Teams 2 onwards
    for i in range(1, group_size):

        print(i)

        if i == 1:
            nations_2 = nations[12 * i:12 * i + 12].sort_values('Confederation', ascending=False).reset_index(drop=True)
        if i == 2:
            nations_2 = nations[12 * i:12 * i + 12].sort_values('Confederation', ascending=True).reset_index(drop=True)
        if i == 3:
            nations_2 = nations[12 * i:12 * i + 12].sort_values('Confederation', ascending=False).reset_index(drop=True)

        complete = 0
        unassigned = list(range(12))

        while complete == 0:

            try:

                for j in range(12):

                    attempt = 0
                    drawn = 0
                    drawn_team, drawn_team_conf = nations_2.iloc[j: j + 1], nations_2.loc[j, 'Confederation']

                    while drawn == 0:

                        x = unassigned[attempt]

                        existing_conf = groups[x]["Confederation"].to_list()

                        if (drawn_team_conf == 'UEFA' and existing_conf.count(
                                drawn_team_conf) < 2) or existing_conf.count(
                            drawn_team_conf) == 0:

                            # groups[x] = groups[x].append(drawn_team, ignore_index=True)
                            groups[x] = pd.concat([groups[x], drawn_team])
                            drawn = 1

                            if j == 11:
                                complete = 1
                                break

                            del unassigned[attempt]

                        else:
                            attempt = attempt + 1

                break


            except:

                if complete == 0:
                    unassigned = list(range(12))
                    random.shuffle(unassigned)

                    for k in range(12):
                        groups[k] = groups[k].head(i)

                continue

    for i in range(12):
        groups[i] = groups[i]['Country'].to_list()

    # Print groups once they've actually had a valid draw otherwise it's very confusing...
    group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I",
                   "Group J", "Group K", "Group L"]

    for i in range(group_size):
        print(f"\n\nPot{i + 1}")
        for j in range(group_number):
            time.sleep(settings.delay * 10)
            print(f"\n{group_names[j]}\n{', '.join(groups[j][:i+1])}")

    return groups

#TODO: Remove below, it is only for testing
class Settings:

    def __init__(self, runs, engine, qualifiers, delay, run_number, confederation, stage):
        self.runs = runs
        self.engine = engine
        self.qualifiers = qualifiers
        self.delay = delay
        self.run_number = run_number
        self.confederation = confederation
        self.stage = stage

settings = Settings(int(input('Choose number of simulations: ')), 'detailed_binomial_match', 'full_qualifiers',
                            4, 1, '', 'Round 1')

groups = world_cup_draw(example_teams, settings, 12, 4)
