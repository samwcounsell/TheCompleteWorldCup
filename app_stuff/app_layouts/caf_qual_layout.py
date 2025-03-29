from dash import dcc, html, Input, Output, callback, dash_table, no_update
import dash_bootstrap_components as dbc
import json

def get_caf_qual_layout(groups, matches, filtered_groups, filtered_matches):

    filtered_round1 = [key for key in filtered_groups if 'round1' in key]
    filtered_round2 = [key for key in filtered_matches if 'round2' in key]

    return [

        dbc.Row([  # Round 1

            dbc.Card([
                dbc.CardBody([

                    dbc.Row([
                        dbc.Col([
                            html.P("\n"),
                            html.P(f"key: {key}"),
                            dash_table.DataTable(groups[key].to_dict('records'),
                                                 [{"name": i, "id": i} for i in groups[key].columns],
                                                 sort_action='native', sort_mode='multi')
                        ]) for key in filtered_round1[i:i + 3]
                    ]) for i in range(0, len(filtered_round1), 3)

                ]),
            ]),

        ]),
        dbc.Row([  # Round 2

            dbc.Card([
                dbc.CardBody([

                    dbc.Row([
                        dbc.Col([
                            html.P("\n"),
                            html.P(key),
                            dash_table.DataTable(matches[key].to_dict('records'),
                                                 [{"name": i, "id": i} for i in matches[key].columns[1:]],
                                                 sort_action='native', sort_mode='multi'),

                            html.P(f"{matches[key].to_dict('records')}"),
                            print(matches[key]),
                            print(matches[key].to_dict('records')),
                            html.P(f"Score: {matches[key].iat[0, 1]} {matches[key].iat[0, 2]}:{matches[key].iat[1, 2]} {matches[key].iat[1, 1]}")
                        ]) for key in filtered_round2[i:i + 3]
                    ]) for i in range(0, len(filtered_round2), 3)

                ]),
            ]),
        ]),

    ]
