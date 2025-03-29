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

print(type(groups))
print(type(matches[key]))

print(matches[key])