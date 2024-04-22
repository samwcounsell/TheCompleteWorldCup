from dash import dcc, html, Input, Output, callback
import pandas as pd
import base64
import io, json
from PIL import Image
from dash import dcc, html, Input, Output, callback, dash_table, no_update
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from scipy.stats import binom, bernoulli
import numpy as np
from io import StringIO
import os

import app_stuff.app_figures.home_figures as hfig
from app_stuff.app_components.navigation import simple_navbar

navbar = simple_navbar()

dfs = {}

selected_run_number = 1
path = os.getcwd()
file_path = os.path.join(path, f'app_data/matches_sim{selected_run_number}.json')

# Open the file and read each line
with open(file_path, 'r') as f:
    for line in f:
        # Remove any trailing newline characters
        line = line.rstrip('\n')

        # Convert the JSON string back into a dictionary
        group_dict = json.loads(line)

        # For each key-value pair in the dictionary
        for key, value in group_dict.items():
            # If the key is 'data', convert the JSON string back into a DataFrame
            if key == 'data':
                df = pd.read_json(StringIO(value))
                # Use the 'id' value as the key to store the DataFrame in the dictionary
                dfs[group_dict['id']] = df

#for key in dfs.keys():
#    dfs[key] = dfs[key].reset_index().rename(columns = {'index': 'Country'})

layout = html.Div([

    navbar,

    *[dbc.Row([
        html.P("\n"),
        html.P(key),
        dash_table.DataTable(dfs[key].to_dict('records'), [{"name": i, "id": i} for i in dfs[key].columns], sort_action='native', sort_mode='multi')
    ]) for key in dfs.keys()]

])