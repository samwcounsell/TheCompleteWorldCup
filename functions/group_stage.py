import pandas as pd
import random
import json
import os

#TODO: Put these files and functions in
from functions.worldcup_functions import worldcup_draw


# Main group-stage function containing the sub-functions
def group_stage(data, teams, legs, settings, WC, group_number, group_size):

    # TODO: Send in dict with sim_number, stage and confederation for id of dataframe when saving as json instead of putting it here
    # data is a list containing nation and player data, teams is a list of length group_number * group_size,
    # legs is integer number of times teams play eachother, settings is list of length 2, WC is an integer 0, 1, 2,
    # group_number and group_size are integers
    if WC == 0:
        groups = group_draw(group_number, group_size, teams)

    else:
        groups = worldcup_draw(data, teams, settings)

    names = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E', 'Group F', 'Group G', 'Group H', 'Group I', 'Group J', 'Group K', 'Group L']

    for i in range(len(groups)):
        print(f"\n{names[i]}")
        groups[i] = group_simulation(data, groups[i], legs, settings, WC)

    path = os.getcwd()
    file_path = os.path.join(path, f'app_data/groups_sim{settings.run_number}.json')

    # Convert each DataFrame to a JSON string and append it to the file
    with open(file_path, 'a') as f:
        for i, df in enumerate(groups):
            # Convert the DataFrame to a JSON string
            json_df = df.to_json()

            # Create a dictionary with the identifier as the key and the JSON string as the value
            json_dict = {'id': f'{settings.confederation}{settings.stage}{names[i].replace(' ', '')}', 'data': json_df}

            # Convert the dictionary to a JSON string and write it to the file
            f.write(json.dumps(json_dict) + '\n')


    return groups


def group_draw(group_number, group_size, teams):
    # group number is an integer (number of groups)
    # group size is an integer (number of teams per group)
    # teams is a list

    # list of group names
    group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I",
                   "Group J", "Group K", "Group L"]

    # getting number of groups from group_names list
    groups = group_names[:group_number]

    # selecting number of pots by amount of teams per group
    for i in range(group_size):

        # collecting list of teams in the pot
        pot = teams[group_number * i: (i + 1) * group_number]
        # shuffling the pot
        random.shuffle(pot)

        # drawing number of groups
        for j in range(group_number):

            # if drawing first team it creates list
            if i == 0:
                groups[j] = [pot[j]]

            # otherwise, it appends new team to the list
            else:
                try:
                    groups[j].append(pot[j])
                # If no more teams to add (UEFA) ignore the issue
                except:
                    groups[j].append("dummy")
                    groups[j].remove("dummy")

    # printing the groups
    for i in range(group_number):
        print(f"{group_names[i]}: {', '.join(groups[i])}")

    return groups


def group_simulation(data, teams, legs, settings, WC):
    # creating group table as pandas sim_data frame and displaying empty group table
    group_table = pd.DataFrame(0, index=teams, columns=['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])
    print("\n", group_table)

    # # for odd numbered groups we append a dummy team for correct fixture order
    if len(teams) % 2 != 0:
        teams.append("dummy")

    n = len(teams)

    # number of matchdays to simulate is legs multiplied number of teams minus one
    for j in range(legs * (n - 1)):

        # proof of function working
        print(f"\nRound {j + 1}")

        # number of matches is number of teams / 2
        for i in range(int(n / 2)):

            # fixture scheduling works by having element 0 v element 1 first
            if i == 0:

                # Makes sure teams alternate home and away leg
                if (j % 2) == 0:
                    participants = teams[0:2]
                else:
                    participants = [teams[1], teams[0]]

                # printing as proof of function
                if 'dummy' in participants:
                    pass
                else:
                    data, score = settings.engine(data, participants, WC, settings, 'G', 0, 0)
                    print(f"\nFinal Score: {participants[0]} {score[0]} - {score[1]} {participants[1]}")
                    group_table = match_update(group_table, participants, score)

            # then the remaining teams play from out to in
            else:
                home, away = teams[i + 1], teams[n - i]
                if (j % 2) == 0:
                    participants = [home, away]
                else:
                    participants = [away, home]

                # printing as proof of function
                if 'dummy' in participants:
                    pass
                else:
                    data, score = settings.engine(data, participants, WC, settings, 'G', 0, 0)
                    print(f"\nFinal Score: {participants[0]} {score[0]} - {score[1]} {participants[1]}")
                    group_table = match_update(group_table, participants, score)

        # second element of list moved to back, functions like 2 column system for drawing fixtures where all teams
        # except a fixed team cycle clockwise
        teams.insert(1, teams.pop())
        group_table = round_update(group_table)

    # return final group table
    print("\n", group_table)
    return group_table


def match_update(group_table, participants, score):
    # Result dependent updates
    if score[0] > score[1]:
        group_table.loc[participants[0], ['Pts', 'W']] += [3, 1]
        group_table.loc[participants[1], 'L'] += 1

    if score[0] < score[1]:
        group_table.loc[participants[1], ['Pts', 'W']] += [3, 1]
        group_table.loc[participants[0], 'L'] += 1

    if score[0] == score[1]:
        group_table.loc[participants, ['Pts', 'D']] += 1

    # Required updates (Home) #TODO: Change output in match_engine to be one array instead of nested arrays of length 1
    group_table.loc[participants, 'P'] += 1
    group_table.loc[participants[0], ['GF', 'GA']] += score
    group_table.loc[participants[1], ['GF', 'GA']] += score[::-1]

    return group_table


def round_update(group_table):
    group_table['GD'] = group_table['GF'] - group_table['GA']
    group_table = group_table.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])

    return group_table





# Variable Glossary
# group_names - list of group names, also used as variable generate groups variable from
# groups - list containing all groups which are themselves lists stored within the list 'groups'
# pot - contains group_number teams, seeded group that teams are distributed into the groups from, one team per pot goes into each group
# group_number - number of groups
# group_size - number of teams in each group
