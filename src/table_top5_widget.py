import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import altair as alt
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# ----------------------------------------------------------------------------------------------
# Read in global data
df = pd.read_csv("../data/processed/df_tidy.csv")
df_2020 = df.loc[df['Year'] == 2020]

# ----------------------------------------------------------------------------------------------
# The structure of the page

app.layout = html.Div([
       # The name of the dashboard
        dbc.Row(dbc.Col(html.H2("Happiness Navigator",),
                        width={'size': 6, 'offset': 1},
                        ),
                ),
        dbc.Row(dbc.Col(html.Div(html.Br(),),)  # Extra space
                ),
        # The years to choose (only one year can be chosen !!!but not working now)
        dbc.Row(dbc.Col(html.Div([
                                html.H3('Years:'),
                                dbc.Button("2015", color="warning", id="btn_2015", className="mr-1"),
                                dbc.Button("2016", color="warning", id="btn_2016", className="mr-1"),
                                dbc.Button("2017", color="warning", id="btn_2017", className="mr-1"),
                                dbc.Button("2018", color="warning", id="btn_2018", className="mr-1"),
                                dbc.Button("2019", color="warning", id="btn_2019", className="mr-1"),
                                dbc.Button("2020", color="warning", id="btn_2020", className="mr-1"),
                                html.Br(),
                                ]
                               ),
                        width={'size': 8, 'offset': 4},
                        ),
                ),
        # The slider, the map, the legend and the top-5 countries table
        dbc.Row(
            [
                dbc.Col(dcc.Slider(id='my-slider',
                                   min=0,
                                   max=10,
                                   step=1,
                                   value=5,
                                   ),
                    
                        width={'size': 3, "offset": 0, 'order': 1}
                        ),
                dbc.Col(dcc.Graph(figure=px.choropleth()),
                        width={'size': 6, "offset": 0, 'order': 2}
                        ),
                dbc.Col(html.Div([html.H3('Top-5 Countries'),
                                 dash_table.DataTable(id='table',
                                                      columns=[{'name': 'Rank', 'id': 'Happiness_rank', 'editable': False, 'selectable': False},
                                                                {'name': 'Country', 'id': 'Country', 'editable': False},
                                                                {'name': 'Happiness score', 'id': 'Happiness_score', 'editable': False},
                                                                {'name': 'GDP per capita', 'id': 'GDP_per_capita', 'editable': False},
                                                                {'name': 'Social support', 'id': 'Social_support', 'editable': False},
                                                                {'name': 'Life expectancy', 'id': 'Life_expectancy', 'editable': False},
                                                                {'name': 'Freedom', 'id': 'Freedom', 'editable': False},
                                                                {'name': 'Generosity', 'id': 'Generosity', 'editable': False},
                                                                {'name': 'Corruption', 'id': 'Corruption', 'editable': False},
                                                                {'name': 'Year', 'id': 'Year', 'editable': False},
                                                                        ],
                                                      data=df_2020.to_dict('records'),
                                                      #fixed_rows={'data': 0},
                                                      #style_data_conditional=(),
                                                      style_cell_conditional=[{'if': {'column_id': 'Happiness_score',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'GDP_per_capita',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Social_support',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Life_expectancy',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Freedom',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Generosity',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Corruption',},
                                                                                'display': 'None',},
                                                                                {'if': {'column_id': 'Year',},
                                                                                'display': 'None',}],
                                                      style_table={'height': 280,
                                                                   'overflowY': 'scroll',
                                                                   'width': 400,
                                                                   },
                                                      style_header = {'display': 'none'},
                                                      style_cell={'textAlign': 'center',
                                                                  'backgroundColor':'#FFC14D',
                                                                  'fontWeight': 'bold',
                                                                  'font-size': '20px',
                                                                  'height': 50,
                                                                  },
                                                      style_as_list_view=True,
                                )
                ]),
                                width={'size': 2,  "offset": 0, 'order': 3}
                        ),
            ],
        ),
        # The plots
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='mybar-1', figure={}),
                        width=3, lg={'size': 3,  "offset": 1,}
                        ),
                dbc.Col(dcc.Graph(id='mybar-2', figure={}),
                        width=3, lg={'size': 3,  "offset": 0,}
                        ),
                dbc.Col(dcc.Graph(id='mybar-3', figure={}),
                        width=3, lg={'size': 3,  "offset": 0,}
                        ),
            ]
        )
])
# ----------------------------------------------------------------------------------------------

# @app.callback(
#     Output(component_id='mybar-1', component_property='figure'),
#     Input(component_id='table', component_property='active_cell')
# )
# def table_to_graph(active_cell):
#     if active_cell is None:
#         df_2020['Happiness_rank'] = '1'
#     elif df_2020[column_id] == 'Country' and active_cell:
#         fig = px.bar(df_2020, x='Country', y='Freedom')
#     return fig



@app.callback(
    Output(component_id='mybar-1', component_property='figure'),
    Input(component_id='table', component_property='derived_virtual_data')
)
def table_to_graph(row_data):
    df_table = df_2020 if row_data is None else pd.DataFrame(row_data)
    fig = px.bar(df_2020, x='Country', y='Freedom')
    return fig

# ----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)