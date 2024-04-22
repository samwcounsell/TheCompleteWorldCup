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
                        dcc.Graph(id='binomial_dists')# Binomial Graph
                    ]),

                ], style={'border-radius': '0px'}),

            ]),
            dbc.Row([

                dbc.Col([

                    dbc.Row([
                        html.P('Home Attack: '),
                        dcc.Slider(0, 2, 0.1, marks={0: '0', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                   value=1, id='ha_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                    dbc.Row([
                        html.P('Home Defense: '),
                        dcc.Slider(0, 2, 0.1, marks={0: '0', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                   value=1, id='hd_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),

                ]),
                dbc.Col([
                    dbc.Row([
                        html.P('Away Attack: '),
                        dcc.Slider(0, 2, 0.1, marks={0: '0', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                   value=1, id='aa_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                    dbc.Row([
                        html.P('Away Defense: '),
                        dcc.Slider(0, 2, 0.1, marks={0: '0', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                   value=1, id='ad_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),

                ]),

            ]),

            dbc.Row([

                html.Div(id='result_probs', style={'fontSize': 14}, className='text-center')

            ])

        ]),
        dbc.Col([  # RHS

        ]),

    ]),

])


# Binomial Graph Callback
@callback(
    [Output('binomial_dists', 'figure'),
     Output('result_probs', 'children')],
    [Input('ha_slider', 'value'),
     Input('hd_slider', 'value'),
     Input('aa_slider', 'value'),
     Input('ad_slider', 'value')]
)
def binomial_graph_update(ha, hd, aa, ad):
    ph, pa = ha / (ad * 90), aa / (hd * 90)
    n = 90
    x = list(range(101))

    pmf_home = binom.pmf(x, n, ph)
    pmf_away = binom.pmf(x, n, pa)
    cdf_away = binom.cdf(x, n, pa)

    home_lt10 = pmf_home[:10]
    home_10plus = np.sum(pmf_home[-91:])
    plot_pmf_home = np.append(home_lt10, home_10plus)

    away_lt10 = pmf_away[:10]
    away_10plus = np.sum(pmf_away[-91:])
    plot_pmf_away = np.append(away_lt10, away_10plus)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(11)), y=plot_pmf_home, name='Home Goals Scored', marker_color='peru'))
    fig.add_trace(go.Bar(x=list(range(11)), y=plot_pmf_away, name='Away Goals Scored', marker_color='darkkhaki'))
    fig.update_layout(
        title={
            'text': "Probability of scoring x goals in 90 minutes",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title='Goals Scored per 90 minutes',
        yaxis_title='Probability',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(ticktext=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '10+'], tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    draw_prob, home_win_prob = 0, 0
    for i in x:
        draw_prob += pmf_home[i] * pmf_away[i]
    for i in x[:-1]:
        home_win_prob += pmf_home[i + 1] * cdf_away[i]
    away_win_prob = 1 - home_win_prob - draw_prob

    return fig, f'Probability of: Home Win = {round(home_win_prob, 3)}, Draw = {round(draw_prob, 3)}, Away Win = {round(away_win_prob, 3)}'
