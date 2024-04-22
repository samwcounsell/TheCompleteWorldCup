from dash import Dash, dcc, html, Input, Output, callback
from app_stuff.app_pages import home, binomial_demo, groups, matches, qualifiers, stochastic_demo
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Updating app_stuff when user selects specific page
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/groups':
        return groups.layout
    elif pathname == '/binomial':
        return binomial_demo.layout
    elif pathname == '/stochastic':
        return stochastic_demo.layout
    elif pathname == '/matches':
        return matches.layout
    elif pathname == '/qualifiers':
        return qualifiers.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)