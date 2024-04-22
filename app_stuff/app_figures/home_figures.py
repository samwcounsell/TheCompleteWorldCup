import plotly.express as px
import pandas as pd

stadiums = pd.read_csv('app_stuff/app_data/stadiums.csv')

stadium_map = px.scatter_mapbox(stadiums, lat='Lat', lon='Lon', zoom=2.3, center={'lat': 34.85, 'lon': -101.67},
                                mapbox_style='open-street-map', color='Nation',
                                color_discrete_sequence=['peru', 'sienna', 'darkkhaki'])
stadium_map.update_traces(hoverinfo='none', hovertemplate=None, marker_size=10)
stadium_map.update_layout(showlegend=False, margin={'r':0, 'l':0, 't':0, 'b':0})