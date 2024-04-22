from dash import dcc, html, Input, Output, callback
import pandas as pd
import base64
import io
from PIL import Image
from dash import dcc, html, Input, Output, callback, dash_table, no_update
import dash_bootstrap_components as dbc

import app_stuff.app_figures.home_figures as hfig
from app_stuff.app_components.navigation import simple_navbar

#TODO: Remove this as it is temporary
df = pd.read_csv('app_data/sim_player_data.csv ')

navbar = simple_navbar()

layout = html.Div([

    navbar,

    dbc.Row([
        dbc.Col([
            dbc.Card([

                dbc.CardBody([
                    dcc.Graph(id='stadium_map', figure=hfig.stadium_map),
                    dcc.Tooltip(id='tooltip', direction='bottom', background_color='papayawhip',
                    border_color='peru')
                ]),

            ]),
        ]),
        dbc.Col([ #TODO: Remove this as it is temporary

            dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], sort_action='native', sort_mode='multi')

        ])
    ])

])

# Data
stadiums = pd.read_csv('app_stuff/app_data/stadiums.csv')

# Callbacks
@callback(
    Output('tooltip', 'show'),
    Output('tooltip', 'bbox'),
    Output('tooltip', 'children'),
    Output('tooltip', 'direction'),
    Input('stadium_map', 'hoverData')
)
def display_stadium(hoverData):

    if hoverData is None:
        return False, no_update, no_update, no_update

    pt = hoverData['points'][0]
    num = stadiums.loc[stadiums['Lat'] == pt['lat']].index[0]
    df_row = stadiums.iloc[num]
    image_path = df_row['Image']
    im = Image.open(f'assets/stadiums/{image_path}')

    buffer = io.BytesIO()
    im.save(buffer, format='jpeg')
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    im_url = 'data:image/jpeg;base64, ' + encoded_image

    hover_data = hoverData['points'][0]
    bbox = hover_data['bbox']

    children = [
        html.Img(src=im_url, style={'width': '100%', 'display': 'block', 'margin': 0}),
        html.P(df_row['Name'], style={'margin': 0}),
        html.P(f'City: {df_row["City"]}', style={'margin': 0}),
        html.P(f'Capacity: {df_row["Capacity"]}', style={'margin': 0}),
    ]

    direction = 'bottom'

    return True, bbox, children, direction