from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout


def caf(data, settings):

    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'caf'

    confederation_introduction("CAF", data)

    # TODO: Tidy this bit up
    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'CAF']['Country'].to_list()

    # Round 1
    print("\nWelcome to CAF Qualifying Round 1")
    settings.stage = 'round1'
    groups = group_stage(data, teams, 2, settings, 0, 9, 6)
    qualified_wc, qualified_b = progression(groups, 9, 4)
    print(qualified_b)
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the next Round: {', '.join(qualified_b)}")

    # Round 2
    print("\nWelcome to CAF Qualifying Round 2")
    settings.stage = 'round2'
    # sim_data, teams, legs, sim, WC, group number, group size
    qualified_c = knockout(data, qualified_b, 1, settings, 0)
    qualified_icp = knockout(data, qualified_c, 1, settings, 0)
    print(f"\nQualified for the Inter-Continental Playoff: {', '.join(qualified_icp)}")

    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the Inter-Continental Playoff: {', '.join(qualified_icp)}")

    # Awards
    confederation_awards("CAF", data, settings)

    return qualified_wc, qualified_icp
