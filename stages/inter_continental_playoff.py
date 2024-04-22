from functions.knockout import knockout


def icp(data, teams, settings):

    settings.confederation = 'icp'
    settings.stage = 'round1'

    df = data[0].loc[data[0]['Country'].isin(teams)][['Country', 'Confederation', 'World Rank']].sort_values(
        'World Rank')

    teams = df['Country'].tolist()
    teams_r1 = teams[-4:]
    order = [0, 3, 1, 2]
    teams_r1 = [teams_r1[i] for i in order]

    print("\nWelcome to the Inter-Continental Playoff")
    print("\nSemi-Finals")

    qualified_a = knockout(data, teams_r1, 1, settings, 0)

    print(qualified_a)
    print(teams)
    teams = teams[:2]
    print(teams)
    teams_r2 = teams + qualified_a
    teams_r2 = [teams_r2[i] for i in order]

    print("\nFinals")

    icp_winners = knockout(data, teams_r2, 1, settings, 0)

    print(f"\nQualified for the World Cup: {', '.join(icp_winners)}")

    return icp_winners
