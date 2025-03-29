import numpy as np
def stochastic_match(data, participants, WC, settings, stage, leg, ET):

    nation_df, player_df = data[0], data[1]
    home, away = participants[0], participants[1]

    scorers = []
    assisters = []

    # TODO: Generate stochastic matrix [hg, hc, hp, hk, c, ak, ap, ac, ag]
    matrix = np.array([])

    states = []
    initial_state = 3 # Home team kicks-off
    time = 0
    score = []
    corners = []

    # TODO: Run 90 minutes

    while time <= n:

        states.append(initial_state)

        new_state = np.random.choice(np.arange(matrix, 1, p = matrix[initial_state, :]))[0]

        # TODO: If new state is corner or goal add accordingly

        initial_state = int(new_state)

        time += 1

    # TODO: Run 30 minutes for ET

    # TODO: Generate scorers and assisters

    # TODO: Export match states