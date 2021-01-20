import dash
import dash_html_components as html
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------------------------------------------------------------------------------------

app.layout = dbc.Container(
    [
        html.H1(),
        # Top screen (logo, years, smiley face)
        dbc.Row(
            [
                dbc.Col(html.H1("Logo"), md=2),
                dbc.Col(html.H1("Years"), md=8),
                dbc.Col(html.H1("Smiley Face"), md=2),
            ]
        ),
        # Main screen layout
        dbc.Row(
            [
                dbc.Col(
                    #slider = dbc.FormGroup(
                        [
                            html.H2('World Happiness Rankings:'),
                            dbc.Label("Health"),
                            dcc.Slider(id="slider_health", min=0, max=10, step=1, value=5, marks={0: '0', 5: '5', 10: '10'}),
                            dbc.Label("Freedom"),
                            dcc.Slider(id="slider_free", min=0, max=10, step=1, value=5, marks={0: '0', 5: '5', 10: '10'}),
                            dbc.Label("Economy"),
                            dcc.Slider(id="slider_econ", min=0, max=10, step=1, value=5, marks={0: '0', 5: '5', 10: '10'}),
                            html.Button('Reset', id='reset_button', n_clicks=0),
                        ]
                    #)
                ),

                dbc.Col(html.H1("Map"), md=6),

                dbc.Col(
                    [
                        html.H2('Top 5 Countries:'),
                        dcc.Textarea(id="list_text")
                        #html.Div(id='result') # Output('result', 'children'),
                    ]
                    #html.H1("Top Countries List"), md=3),
                )
            ]
        ),
        # Global metrics and individual country plots
        dbc.Row(
            [
                dbc.Col(html.H1("Plot1"), md=4),
                dbc.Col(html.H1("Plot2"), md=4),
                dbc.Col(html.H1("Plot3"), md=4),
                
            ]
        ),
    ]
)

# ----------------------------------------------------------------------------------------------

# Import happiness dataset (2020 for now)
happiness_data = pd.read_csv("data/raw/2020.csv")
happiness_df = pd.DataFrame(happiness_data)


# ----------------------------------------------------------------------------------------------

# Slider Callbacks
@app.callback(
    Output(component_id='list_text', component_property='value'),
    Input('slider_health', 'value'), # add more inputs? but then how do you send them to the function?
    Input('slider_free', 'value'),
    Input('slider_econ', 'value')
)

def country_list(value_health, value_free, value_econ, data=happiness_data):
    data = [['Healthy life expectancy', value_health], ['Freedom to make life choices', value_free], ['Logged GDP per capita', value_econ]]
    country_df = pd.DataFrame(data, columns = ['Measure', 'Value'])
    country_df = country_df.sort_values(by=['Value'], ascending = False)
    col_name = country_df.iloc[0,0]
    filtered_data = happiness_df.sort_values(by=[col_name]) # filter data somehow (sort by whatever value is most important)

    country_list = filtered_data.iloc[:,0]
    return str(country_list[0:5])

# Reset Button Callback, reset back to 5
@app.callback(
    Output('slider_health','value'),
    Output('slider_free','value'),
    Output('slider_econ','value'),
    [Input('reset_button','n_clicks')])

def update(reset):
    return 5, 5, 5

# ----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
