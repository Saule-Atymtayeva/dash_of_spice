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
                dbc.Col(html.Div(dash_table.DataTable(id='table',
                                                      columns=[{'name': i, 'id': i} for i in df_2020.loc[:,['Happiness_rank','Country']]],
                                                      data=df_2020.to_dict('records'),
                                                      #fixed_rows={'data': 0},
                                                      #style_data_conditional=(),
                                                      style_table={'height': 280,
                                                                   'overflowY': 'scroll',
                                                                   'width': 400,
                                                                   },
                                                      style_header = {'display': 'none'},
                                                      style_cell={'textAlign': 'center',
                                                                  'backgroundColor':'#FFC14D',
                                                                  'fontWeight': 'bold',
                                                                  #'font-family': 'cursive',
                                                                  'font-size': '20px',
                                                                  #'minWidth': 95,
                                                                  'height': 50,
                                                                  #'maxWidth': 95,
                                                                  
                                                                  },
                                                      #style_data = {'border': 'none'},
                                                      style_as_list_view=True,
                                                      )
                                                      ),
                        width={'size': 2,  "offset": 0, 'order': 3}
                        ),
            ],
        ),
        # The plots
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='pie_chart1', figure={}),
                        width=3, lg={'size': 3,  "offset": 1,}
                        ),
                dbc.Col(dcc.Graph(id='pie_chart2', figure={}),
                        width=3, lg={'size': 3,  "offset": 0,}
                        ),
                dbc.Col(dcc.Graph(id='pie_chart3', figure={}),
                        width=3, lg={'size': 3,  "offset": 0,}
                        ),
            ]
        )
],
#style={"borderStyle":{"width":"10px", "color":"black"}}

)

# ----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)