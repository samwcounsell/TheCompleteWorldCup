from match_engines.binomial.binomial_detailed import detailed_binomial_match

# TODO; Remove these, this is for testing only
def simple_binomial_match(): print('hi')
def full_qualifiers(): return 20


class Settings:

    def __init__(self, runs, engine, qualifiers, delay, run_number, confederation, stage):
        self.runs = runs
        self.engine = engine
        self.qualifiers = qualifiers
        self.delay = delay
        self.run_number = run_number
        self.confederation = confederation
        self.stage = stage


def set_up():
    while True:
        try:
            choice = int(input(
                f'\nChoose simulation type (1. binomial_detailed 2. binomial_simple 3. binomial_realistic 4. stochastic):   '))
            if 1 <= choice <= 4:
                break
            else:
                continue
        except:
            print('Dont be cheeky, enter either 1, 2, 3 or 4. You have been warned...')

    if choice == 1:
        settings = Settings(int(input('Choose number of simulations: ')), detailed_binomial_match, full_qualifiers,
                            float(input('Choose delay for qualifiers, 0 is reccomended: ')), 1, '', 'Round 1')
    elif choice == 2:
        settings = Settings(int(input('Choose number of simulations: ')), simple_binomial_match, full_qualifiers,
                            0, 1, '', 'Round 1')
    elif choice == 3:
        settings = Settings(1, detailed_binomial_match, full_qualifiers,
                            float(input('Choose delay for qualifiers, 0 is reccomended: ')), 1, '', 'Round 1')
    else:
        settings = Settings(int(input('Choose number of simulations: ')), detailed_binomial_match, full_qualifiers,
                            4, 1, '', 'Round 1')

    return settings
