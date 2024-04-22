from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout


def uefa(data, settings):
    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'uefa'

    confederation_introduction("UEFA", data)

    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'UEFA']['Country'].to_list()

    # Round 1
    print("\nWelcome to UEFA Qualifying Round 1")
    settings.stage = 'round1'
    # sim_data, teams, legs, sim, WC, group number, group size
    groups = group_stage(data, teams, 2, settings, 0, 12, 5)
    qualified_wc, qualified_b = progression(groups, 12, 12)
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the next Round: {', '.join(qualified_b)}")

    # Round 2, going off script here because no nations league
    print("\nWelcome to UEFA Qualifying Round 2")
    settings.stage = 'round2'
    # sim_data, teams, legs, sim, WC, group number, group size
    groups = group_stage(data, qualified_b, 2, settings, 0, 4, 3)
    qualified_wc2, qualified_d = progression(groups, 4, 0)

    print(f"\nQualified for the World Cup: {', '.join(qualified_wc2)}")
    qualified_wc += qualified_wc2

    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    # Awards
    confederation_awards("UEFA", data, settings)

    return qualified_wc
