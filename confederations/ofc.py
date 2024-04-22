from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout


def ofc(data, settings):

    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'ofc'

    confederation_introduction("OFC", data)

    # TODO: Tidy this bit up
    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'OFC']['Country'].to_list()

    # Round 1
    print("\nWelcome to OFC Qualifying Round 1")
    settings.stage = 'round1'
    qualified = knockout(data, teams[-4:], 1, settings, 0)
    qualified_a = knockout(data, qualified, 1, settings, 0)

    teams = teams[:-4]
    teams.extend(qualified_a)

    # Round 2
    print("\nWelcome to OFC Qualifying Round 2")
    settings.stage = 'round2'
    # sim_data, teams, legs, sim, WC, group number, group size
    groups = group_stage(data, teams, 2, settings, 0, 2, 4)
    qualified_b, qualified_c = progression(groups, 4, 0)
    print(f"\nQualified: {', '.join(qualified_b)}")

    # Round 3
    print("\nWelcome to OFC Qualifying Round 3")
    settings.stage = 'round3'
    # Reordering teams to ensure correct matchups
    order = [0, 3, 1, 2]
    teams = [qualified_b[i] for i in order]
    qualified_d = knockout(data, teams, 1, settings, 0)
    print("\nOFC Qualifying Final")
    qualified_wc = knockout(data, qualified_d, 1, settings, 0)
    for country in qualified_wc:
        if country in qualified_d:
            qualified_d.remove(country)
    qualified_icp = qualified_d
    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the Inter-Continental Playoff: {', '.join(qualified_icp)}")

    # Awards
    confederation_awards("OFC", data, settings)

    return qualified_wc, qualified_icp