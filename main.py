#TODO: If a json exists in the app_data before starting sim, delete it


import pandas as pd
from functions.settings import set_up

settings = set_up()

from stages.qualifiers import complete_qualifiers

nation_data, player_data = pd.read_csv('data/nation_data.csv'), pd.read_csv('data/player_data.csv')
data = [nation_data, player_data]

data, wc_teams = complete_qualifiers(data, settings)

data[0].to_csv('app_data/sim_nation_data.csv')
data[1].to_csv('app_data/sim_player_data.csv')

