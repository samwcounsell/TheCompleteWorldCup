# This can be used to define rule sets for#
# the simulation and be used throughout the world cup to remove need for if statements based on type


def add(x, y):

    return x + y


def sub(x, y):

    return x - y



class MyClass:

    def __init__(self, a, b, funct):
        self.i = a
        self.j = b
        self.f = funct


def math(x, y, z):

    print(x.f)

    return x.f(y, z)

x = MyClass(1, 2, add)
y = MyClass(2, 7, add)
z = MyClass(7, 1, sub)

rule_sets = {'x': x, 'y': y, 'z': z}

c = input('Choose rules: ')

rules = rule_sets.get(c)

print(math(rules, 3, 4))

# Settings class to be used instead of if statements when calling for things like the Match Engine
class Settings:

    def __init__(self, runs, qualifying, match_engine):

        self.runs = runs
        self.qualifying = qualifying # Name of qualifying function
        self.match_engine = match_engine # Name of match engine

# List of Settings
basic_fast = Settings(n, full_qualifiers, binomial_quick)
basic_slow = Settings(n, full_qualifiers, binomial_full)
realistic = Settings(1, no_qualifiers, binomial_full)
stochastic = Settings(n, full_qualifiers, stochastic_full)

