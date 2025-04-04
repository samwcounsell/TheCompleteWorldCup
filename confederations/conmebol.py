from functions.presentation_functions import confederation_introduction, confederation_awards
from functions.group_stage import group_stage
from functions.progression import progression


def conmebol(data, settings):

    # TODO: Add if loop for running more than one simulation
    settings.confederation = 'conmebol'

    confederation_introduction("CONMEBOL", data)

    # TODO: Tidy this bit up
    nation_df = data[0]
    teams = nation_df.loc[nation_df['Confederation'] == 'CONMEBOL']['Country'].to_list()

    # Round 1
    print("\nWelcome to CONMEBOL Qualifying")
    settings.stage = 'round1'
    # sim_data, teams, legs, sim, WC, group number, group size
    groups = group_stage(data, teams, 2, settings, 0, 1, len(teams))
    qualified_wc, qualified_icp = progression(groups, 6, 1)

    print(f"\nQualified for the World Cup: {', '.join(qualified_wc)}")
    print(f"\nQualified for the Inter-Continental Play Off: {''.join(qualified_icp)}")

    # Awards
    confederation_awards("CONMEBOL", data, settings)

    return qualified_wc, qualified_icp