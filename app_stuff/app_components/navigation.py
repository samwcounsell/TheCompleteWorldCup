import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from PIL import Image

WC_logo = 'app_stuff/app_assets/logos/WC_Logo.png'
html.Img(src=r'app_stuff/app_assets/logos/WC_Logo.png', alt='image')

def simple_navbar():

    navbar = dbc.NavbarSimple(
        children = [
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Binomial Engine Explainer", href='/binomial'),
                    dbc.DropdownMenuItem("Stochastic Engine Explainer", href='/stochastic'),
                    dbc.DropdownMenuItem("Groups", href='/groups'),
                    dbc.DropdownMenuItem("Matches", href='/matches'),
                    dbc.DropdownMenuItem("Qualifiers", href='/qualifiers'),
                ],
            ),
        ],
        color="dark",
        dark=True,
    )

    return navbar