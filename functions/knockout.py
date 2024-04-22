from scipy.stats import bernoulli


def knockout(data, teams, legs, settings, WC):

    qualified = []

    for i in range(int(len(teams) / 2)):

        score = [0, 0]

        for j in range(legs):

            # Makes sure teams alternate home and away leg
            if (j % 2) == 0:
                participants = teams[2 * i: 2 * i + 2]
            else:
                participants = [teams[2 * i + 1], teams[2 * i]]

            # Running the match
            data, leg_score = settings.engine(data, participants, WC, settings, 'K', j, 0)

            print(f"\nFinal Score: {participants[0]} {leg_score[0]} - {leg_score[1]} {participants[1]}")

            if (j % 2) != 0:
                leg_score.reverse()

            score = [a + b for a, b in zip(score, leg_score)]
            participants = teams[2 * i: 2 * i + 2]

        if legs > 1:
            print(f"\nAggregate Score: {participants[0]} {score[0]} - {score[1]} {participants[1]}")

        if score[0] > score[1]:
            qualified.append(participants[0])

        elif score[1] > score[0]:
            qualified.append(participants[1])

        else:
            data, leg_score = settings.engine(data, participants, WC, settings, 'ET', 0, 1)

            # print(f"\nET Final Score: {participants[0]} {score[0]} - {score[1]} {participants[1]}")
            score = [a + b for a, b in zip(score, leg_score)]
            print(f"\nET Final Score: {participants[0]} {score[0]} - {score[1]} {participants[1]}")

            if score[0] > score[1]:
                qualified.append(participants[0])

            elif score[1] > score[0]:
                qualified.append(participants[1])

            else:
                pen_winner = penalties()
                qualified.append(participants[pen_winner])

    return qualified


def penalties():
    # Run penalty shootout (Move to knockout stage)
    pen_home, pen_away = sum(bernoulli.rvs(0.7, size=5)), sum(bernoulli.rvs(0.7, size=5))

    # If level after 5 penalties
    if pen_home == pen_away:
        while pen_home == pen_away:
            pen_home, pen_away = int(pen_home + bernoulli.rvs(0.7, size=1)), int(pen_away + bernoulli.rvs(0.7, size=1))

    if pen_home > pen_away:
        winner = 0

    else:
        winner = 1

    print(f"\nPenalties: {pen_home} - {pen_away}")

    return winner
