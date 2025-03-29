from functions.group_stage import group_stage
from functions.progression import progression
from functions.knockout import knockout
# World Cup Draw

# Group Stage

# Ro32

# Ro16

# QF

# SF

# F

def world_cup_finals(data, settings, teams):

    settings.confederation = 'Finals'
    settings.stage = 'Group Stage'
    settings.WC = 1

    # Group Stage
    print("\nWelcome to World Cup Group Stage")
    groups = group_stage(data, teams, 1, settings, 1, 12, 4)

    qualified_top2, qualified_third = progression(groups, 24, 8)
    qualified = qualified_top2.extend(qualified_third)
    print(f"\nQualified for the Round of 32: {', '.join(qualified)}")

    # Reorder 32 teams, so they're in correct format for knockout
    order = [4, -1, 8, -1, 12, 13, 5, 14, 22, 23, 7, 21, 3, -1, 6, -1, 2, 17, 16, 20, 0, -1, 11, -1, 9, 19, 15, 18, 1, -1, 10, -1]
    order_b = list(range(24, 32))
    # This replaces the -1 values with the teams qualified in third place, to ensure they enter the correct part of
    # the bracket
    b = 0
    for i in range(len(order)):
        if order[i] == -1:
            order[i] = order_b[b]
            b += 1

    qualified_ro32 = [qualified[i] for i in order]

    # TODO: (later) also properly configure the 3rd place teams so that they don't play teams from their own group (it's a very weird system they're using)
    # TODO: (continued), as I will need to update progression to store info on what group they came from

    # Round of 32
    print("\nWelcome to the Round of 32")
    settings.stage = 'roundof32'
    qualified_ro16 = knockout(data, qualified_ro32, 1, settings, 1)
    print(qualified_ro16)

    # Round of 16
    print("\nWelcome to the Round of 16")
    settings.stage = 'roundof32'
    qualified_qf = knockout(data, qualified_ro16, 1, settings, 1)
    print(qualified_ro16)

    # Quarter Finals
    print("\nWelcome to the Quarter-Finals")
    settings.stage = 'roundof32'
    qualified_sf = knockout(data, qualified_qf, 1, settings, 1)
    print(qualified_ro16)

    # Semi-Finals
    print("\nWelcome to the Semi-Finals")
    settings.stage = 'roundof32'
    qualified_f = knockout(data, qualified_sf, 1, settings, 1)
    print(qualified_ro16)

    # Final
    print("\nWelcome to the Final")
    settings.stage = 'roundof32'
    winner = knockout(data, qualified_f, 1, settings, 1)
    print(winner)

    return data


#TODO: Testing to be removed
#example_teams = ['USA', 'Mexico', 'Canada', 'Iraq', 'Saudi Arabia', 'Iran', 'Uzbekistan', 'Japan', 'South Korea', 'Bahrain', 'UAE', 'Algeria', 'Nigeria', 'Senegal', 'Mali', 'Cameroon', 'Ghana', 'Tunisia', 'Madagascar', 'Gabon', 'Jamaica', 'El Salvador', 'Costa Rica', 'Brazil', 'Uruguay', 'Colombia', 'Argentina', 'Ecuador', 'Chile', 'New Zealand', 'Italy', 'England', 'Germany', 'Portugal', 'Czechia', 'Bulgaria', 'France', 'Belgium', 'Poland', 'Spain', 'Netherlands', 'North Macedonia', 'Sweden', 'Switzerland', 'Denmark', 'Austria', 'Curacao', 'Jordan']

#import pandas as pd
#nation_data, player_data = pd.read_csv('../data/nation_data.csv'), pd.read_csv('../data/player_data.csv')
#data = [nation_data, player_data]

#class Settings:

#    def __init__(self, runs, engine, qualifiers, delay, run_number, confederation, stage):
#        self.runs = runs
#        self.engine = engine
#        self.qualifiers = qualifiers
#        self.delay = delay
#        self.run_number = run_number
#        self.confederation = confederation
#        self.stage = stage

#settings = Settings(int(input('Choose number of simulations: ')), 'detailed_binomial_match', 'full_qualifiers',
                            #4, 1, '', 'Round 1')

#data = world_cup_finals(data, settings, example_teams)