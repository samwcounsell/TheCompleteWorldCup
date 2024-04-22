import math
import pandas as pd


def progression(groups, a, b):
    x = math.floor(a / len(groups))

    # qualified_a have gone straight through (straight)
    qualified_a, qualified_b = [], []

    for i in range(len(groups)):
        # Adding teams straight qualified to a list
        idx = groups[i].index.to_list()
        qualified_a.extend(idx[:x])

        # Removing qualified teams from groups to allow for extra teams to be calculated
        groups[i] = groups[i].iloc[x:]

    # TODO: Add system for if straight % groups != 0 (sort all next placed teams out) (DONE WITHOUT TESTING)

    # highest scoring next best placed teams
    x2 = a % len(groups)
    if x2 != 0:

        df = pd.DataFrame(columns=['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])

        for i in range(len(groups)):
            df = pd.concat([df, groups[i].head(1)])

        df = df.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])

        idx2 = df.index.to_list()
        qualified_a.extend(idx2[:x2])

        if b != 0:
            del idx2[:x2]
            qualified_b.extend(idx2[:b])


    # Getting x next best teams that go to a different round TODO: Add this above again first for the case that the
    #  number of groups isn't a factor of the number of teams going through to qualified_a section
    if x2 == 0 and b != 0:

        print(b)

        y = math.floor(b / len(groups))

        df = pd.DataFrame(columns=['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])

        if b > len(groups):
            for i in range(len(groups)):
                df = pd.concat([df, groups[i].head(y)])
        else:
            for i in range(len(groups)):
                df = pd.concat([df, groups[i].head(1)])

        df = df.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])

        print(df)
        print(b)

        idx3 = df.index.to_list()
        print(idx3)
        qualified_b.extend(idx3[:b])

    return qualified_a, qualified_b
