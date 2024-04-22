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
from app_stuff.app_layouts.caf_qual_layout import get_caf_qual_layout

navbar = simple_navbar()

groups = {}
matches = {}

selected_run_number = 1
path = os.getcwd()
group_path = os.path.join(path, f'app_data/groups_sim{selected_run_number}.json')
match_path = os.path.join(path, f'app_data/matches_sim{selected_run_number}.json')

# Getting groups
with open(group_path, 'r') as f:
    for line in f:
        # Remove any trailing newline characters
        line = line.rstrip('\n')

        # Convert the JSON string back into a dictionary
        group_dict = json.loads(line)

        # For each key-value pair in the dictionary
        for key, value in group_dict.items():
            # If the key is 'data', convert the JSON string back into a DataFrame
            if key == 'data':
                group = pd.read_json(StringIO(value))
                # Use the 'id' value as the key to store the DataFrame in the dictionary
                groups[group_dict['id']] = group

for key in groups.keys():
    groups[key] = groups[key].reset_index().rename(columns={'index': 'Country'})

# Getting matches
with open(match_path, 'r') as f:
    for line in f:
        # Remove any trailing newline characters
        line = line.rstrip('\n')

        # Convert the JSON string back into a dictionary
        match_dict = json.loads(line)

        # For each key-value pair in the dictionary
        for key, value in match_dict.items():
            # If the key is 'data', convert the JSON string back into a DataFrame
            if key == 'data':
                match = pd.read_json(StringIO(value))
                # Use the 'id' value as the key to store the DataFrame in the dictionary
                matches[match_dict['id']] = match

for key in matches.keys():
    matches[key] = matches[key].reset_index().rename(columns={'index': 'Country'})

layout = html.Div([

    navbar,

    dcc.Tabs(id='confederation_tabs', value='afc', children=[
        dcc.Tab(label='afc_tab', value='afc'),
        dcc.Tab(label='caf_tab', value='caf'),
        dcc.Tab(label='concacaf_tab', value='concacaf'),
        dcc.Tab(label='conmebol_tab', value='conmebol'),
        dcc.Tab(label='ofc_tab', value='ofc'),
        dcc.Tab(label='uefa_tab', value='uefa'),
        dcc.Tab(label='icp_tab', value='icp'),
    ]),

    dbc.Row([

        dbc.Col([

            html.Div(id='confederation_layout'),  # LHS
        ], width=8),

        dbc.Col([

        ], width=4),  # RHS
    ]),

])


@callback(Output('confederation_layout', 'children'),
          Input('confederation_tabs', 'value'))
def confederation_choice(tab):
    # Filtering only records from selected confederation
    filtered_groups = [key for key in groups.keys() if key.startswith(tab)]
    filtered_matches = [key for key in matches.keys() if key.startswith(tab)]

    if tab == 'caf':

        layout = get_caf_qual_layout(groups, matches, filtered_groups, filtered_matches)

        return layout

    else:
        return [
            dbc.Row([
                dbc.Col([
                    html.P("\n"),
                    html.P(key),
                    dash_table.DataTable(groups[key].to_dict('records'),
                                         [{"name": i, "id": i} for i in groups[key].columns],
                                         sort_action='native', sort_mode='multi')
                ]) for key in filtered_groups[i:i + 4]
            ]) for i in range(0, len(filtered_groups), 4)
        ]
