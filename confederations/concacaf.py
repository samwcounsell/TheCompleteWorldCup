from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout


def concacaf(data, settings):

    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'concacaf'

    confederation_introduction("CONCACAF", data)

    # TODO: Tidy this bit up
    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'CONCACAF']['Country'].to_list()
    teams.remove("USA")
    teams.remove("Mexico")
    teams.remove("Canada")

    # Round 1
    print("\nWelcome to CONCACAF Qualifying Round 1")
    settings.stage = 'round1'
    qualified = knockout(data, teams[-4:], 2, settings, 0)
    print(f"\nQualified for the next Round: {', '.join(qualified)}")

    teams = teams[:-4]
    teams.extend(qualified)

    # Round 2
    print("\nWelcome to CONCACAF Qualifying Round 2")
    settings.stage = 'round2'
    groups = group_stage(data, teams, 1, settings, 0, 6, 5)
    qualified_a, qualified_b = progression(groups, 12, 0)

    # Round 3
    print("\nWelcome to CONCACAF Qualifying Round 3")
    settings.stage = 'round3'
    groups = group_stage(data, qualified_a, 2, settings, 0, 3, 4)
    qualified_wc, qualified_icp = progression(groups, 3, 2)
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the Inter-Continental Play Off: {', '.join(qualified_icp)}")

    # Awards
    confederation_awards("CONCACAF", data, settings)

    return qualified_wc, qualified_icp