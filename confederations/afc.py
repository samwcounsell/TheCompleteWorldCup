from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout

def afc(data, settings):

    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'afc'

    confederation_introduction("AFC", data)

    # TODO: Tidy this bit up
    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'AFC']['Country'].to_list()

    # Round 1
    print("\nWelcome to AFC Qualifying Round 1")
    settings.stage = 'round1'
    qualified = knockout(data, teams[25:], 2, settings, 0)

    teams = teams[:25]
    teams.extend(qualified)

    # Round 2
    print("\nWelcome to AFC Qualifying Round 2")
    settings.stage = 'round2'
    # sim_data, teams, legs, sim, WC, group number, group size
    groups = group_stage(data, teams, 2, settings, 0, 9, 4)
    qualified_a, qualified_b = progression(groups, 18, 0)
    print(f"\nQualified for the next Round: {', '.join(qualified_a)}")

    # Round 3
    print("\nWelcome to AFC Qualifying Round 3")
    settings.stage = 'round3'
    groups = group_stage(data, qualified_a, 2, settings, 0, 3, 6)
    qualified_wc, qualified_c = progression(groups, 6, 6)
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the next Round: {', '.join(qualified_c)}")

    # Round 4
    print("\nWelcome to AFC Qualifying Round 4")
    settings.stage = 'round4'
    groups = group_stage(data, qualified_c, 1, settings, 0, 2, 3)
    qualified_wc2, qualified_d = progression(groups, 2, 2)
    qualified_wc += qualified_wc2
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc2)}")
    print(f"\nQualified for the next Round: {', '.join(qualified_d)}")

    # Round 5
    settings.stage = 'round5'
    qualified_icp = knockout(data, qualified_d, 2, settings, 0)

    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the Inter-Continental Play Off: {''.join(qualified_icp)}")

    # Awards
    confederation_awards("AFC", data, settings)

    return qualified_wc, qualified_icp
