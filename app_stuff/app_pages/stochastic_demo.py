from dash import dcc, html, Input, Output, callback
import pandas as pd
import base64
import io
from PIL import Image
from dash import dcc, html, Input, Output, callback, dash_table, no_update
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from scipy.stats import binom, bernoulli
import numpy as np

P = np.array([
    [0.1, 0, 0.1, 0.5, 0.2, 0, 0, 0.1, 0],  # HC
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # HK
    [0.15, 0, 0.5, 0.2, 0.1, 0, 0, 0.05, 0],  # HP
    [0, 0, 0.4, 0.2, 0.4, 0, 0, 0, 0],  # C
    [0, 0, 0.1, 0.2, 0.5, 0, 0.15, 0, 0.05],  # AP
    [0, 0, 0, 0, 1, 0, 0, 0, 0],  # AK
    [0, 0, 0.2, 0.5, 0.1, 0, 0.1, 0, 0.1],  # AC
    [0, 0, 0, 0, 0, 1, 0, 0, 0],  # HG
    [0, 1, 0, 0, 0, 0, 0, 0, 0]  # AG
])

Pn = P

u = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0])
ui = u

expected_visits = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

for i in range(46):
    expected_visits = expected_visits + ui
    Pi = np.dot(P, Pn)
    Pn = Pi
    ui = np.dot(u, Pi)

u = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0])
ui = u
Pn = P

for i in range(46):
    expected_visits = expected_visits + ui
    Pi = np.dot(P, Pn)
    Pn = Pi
    ui = np.dot(u, Pi)

## Now calculating expected transitions for heatmap
y = expected_visits
y[1] -= 1
y[5] -= 1
y *= (44 / 45)
y[1] += 1
y[5] += 1

expected_transitions = P * y[:, np.newaxis]

## Creating the figures
P_fig = px.imshow(P, text_auto=True, color_continuous_scale='ylorbr',
                  labels=dict(x='Transition State', y="Starting State", color="P"),
                  x=['Home Corner', 'Home Kickoff', 'Home Possesion', 'Contested Ball',
                     'Away Possesion', 'Away Kickoff', 'Away Corner', 'Home Goal', 'Away Goal'],
                  y=['Home Corner', 'Home Kickoff', 'Home Possesion', 'Contested Ball',
                     'Away Possesion', 'Away Kickoff', 'Away Corner', 'Home Goal', 'Away Goal'])
P_fig.update_xaxes(side="top")

expected_transitions_fig = px.imshow(np.round(expected_transitions, 2),
                                     text_auto=True,
                                     color_continuous_scale='ylorbr',
                                     labels=dict(x='Transition State', y="Starting State", color="Expected Occurrence"),
                                     x=['Home Corner', 'Home Kickoff', 'Home Possesion', 'Contested Ball',
                                        'Away Possesion', 'Away Kickoff', 'Away Corner', 'Home Goal', 'Away Goal'],
                                     y=['Home Corner', 'Home Kickoff', 'Home Possesion', 'Contested Ball',
                                        'Away Possesion', 'Away Kickoff', 'Away Corner', 'Home Goal', 'Away Goal'])
expected_transitions_fig.update_xaxes(side="top", tickangle=45)
expected_transitions_fig.update_traces(textfont_size=10)
expected_transitions_fig.update_layout(
    coloraxis_colorbar=dict(
        title="Expected<br>Occurrence",  # Use <br> for line break
        titleside="right",
        titlefont=dict(size=10),
        x=0.8 # Adjust this value to move colorbar closer/farther from the plot
    )
)

import app_stuff.app_figures.home_figures as hfig
from app_stuff.app_components.navigation import simple_navbar

navbar = simple_navbar()

layout = html.Div([

    navbar,

    dbc.Row([
        dbc.Col([  # LHS

            dbc.Row([

                dbc.Card([

                    dbc.CardBody([
                        dcc.Markdown(r'''$$
                            \small{
                            P = \qquad \begin{array}{c c} 
                            & \begin{array}{c c c c c c c c c} HC & HK & HP & C & AP & AK & AC & HG & AG \\ \end{array} \\
                            \begin{array}{c c c}HC\\HK\\HP\\C\\AP\\AK\\AC\\HG\\AG  \end{array} &
                            \left[
                            \begin{array}{c c c c c c c c c}
                            1/10 & 0 & 1/10 & 1/2 & 1/5 & 0 & 0 & 1/10 & 0 \\
                            0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0  \\
                            3/20 & 0 & 1/2 & 1/5 & 1/10 & 0 & 0 & 1/20 & 0 \\
                            0 & 0 & 2/5 & 1/5 & 2/5 & 0 & 0 & 0 & 0 \\
                            0 & 0 & 1/10 & 1/5 & 1/2 & 0 & 3/20 & 0 & 1/20 \\
                            0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0  \\
                            0 & 0 & 1/5 & 1/2 & 1/10 & 0 & 1/10 & 0 & 1/10 \\
                            0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0  \\
                            0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0  
                            \end{array}
                            \right]
                            \end{array}
                            }
                            $$''', mathjax=True),
                    ]),

                ], style={'border-radius': '0px'}),

            ]),

        ]),

    ]),

    dbc.Row([
        dbc.Col([  # LHS

            dbc.Row([

                dbc.Card([

                    dbc.CardBody([
                        dcc.Graph(figure=expected_transitions_fig)
                    ]),

                ], style={'border-radius': '0px'}),

            ]),

        ]),
    ]),

])
