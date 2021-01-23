import dash
import dash_html_components as html
import dash_table
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64

data_cn = pd.read_csv("data/processed/cn_tidy.csv")
test = data_cn
test["Global_Average"] = "Global Average"

unique_countries = data_cn["Country"].unique()
country_options = [{"label": c, "value": c} for c in unique_countries]

# for table
df = pd.read_csv("data/processed/df_tidy.csv")
df['Delta_happy'] = df['Happiness_score']
df_2020 = df.loc[df['Year'] == 2020]
world_map = alt.topo_feature(data.world_110m.url, "countries")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server # for heroku

# ----------------------------------------------------------------------------------------------

# Images
image_filename = 'assets/logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = 'assets/smiley.gif'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())
app.layout = dbc.Container(
    [
        html.H1(),
        # Top screen (logo, years, smiley face)
        dbc.Row(
            [
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'60%', 'width':'20%'})),
                dbc.Col(html.H1("The Happiness Navigator"), md=6),
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'height':'60%', 'width':'20%'})),
            ]
        ),
        # Main screen layout
        dbc.Row(
            [
                dbc.Col(
                    # slider = dbc.FormGroup(
                    [
                        html.H2("World Happiness Rankings:"),
                        dbc.Label("Health"),
                        dcc.Slider(
                            id="slider_health",
                            min=0,
                            max=10,
                            step=1,
                            value=5,
                            marks={0: "0", 5: "5", 10: "10"},
                        ),
                        dbc.Label("Freedom"),
                        dcc.Slider(
                            id="slider_free",
                            min=0,
                            max=10,
                            step=1,
                            value=5,
                            marks={0: "0", 5: "5", 10: "10"},
                        ),
                        dbc.Label("Economy"),
                        dcc.Slider(
                            id="slider_econ",
                            min=0,
                            max=10,
                            step=1,
                            value=5,
                            marks={0: "0", 5: "5", 10: "10"},
                        ),
                        html.Button("Reset", id="reset_button", n_clicks=0),
                    ]
                    # )
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="map",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "400px",
                            },
                        )
                    ],
                    md=6,
                ),
                dbc.Col(html.Div([html.H3('Top-5 Countries'),
                                  html.H6('\nHappiness Rank | Country'),
                                 dash_table.DataTable(id='table',
                                                      columns=[{'name': i, 'id': i} for i in df.loc[:,['Happiness_rank','Country']]],
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
            ]
        ),
        # Global metrics and individual country plots
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            [
                                "Choose your y-axis feature!",
                                dcc.Dropdown(
                                    id="yaxis_feature",
                                    value="Happiness_score",
                                    options=[
                                        {
                                            "label": "Happiness Score",
                                            "value": "Happiness_score",
                                        },
                                        {
                                            "label": "GDP Per Capita",
                                            "value": "GDP_per_capita",
                                        },
                                        {
                                            "label": "Social Support",
                                            "value": "Social_support",
                                        },
                                        {
                                            "label": "Life Expectancy",
                                            "value": "Life_expectancy",
                                        },
                                        {"label": "Freedom", "value": "Freedom"},
                                        {"label": "Generosity", "value": "Generosity"},
                                        {"label": "Corruption", "value": "Corruption"},
                                    ],
                                    style={
                                        "border-width": "10",
                                        "width": "200px",
                                        "height": "20px",
                                        "margin": "0px",
                                    },
                                ),
                            ]
                        )
                    ],
                    md=2.5,
                ),
                dbc.Col(
                    html.Label(
                        [
                            "Choose your countries!",
                            dcc.Dropdown(
                                id="country_drop_down",
                                options=country_options,
                                value=["Canada", "United States"],
                                multi=True,
                                style={
                                    "border-width": "10",
                                    "width": "200px",
                                    "height": "20px",
                                    "margin": "0px",
                                },
                            ),
                        ]
                    ),
                    md=3,
                ),
                dbc.Col(
                    html.Iframe(
                        id="country_plot",
                        style={
                            "border-width": "0",
                            "width": "400px",
                            "height": "400px",
                        },
                    ),
                    md=4,
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("country_plot", "srcDoc"),
    Input("yaxis_feature", "value"),
    Input("country_drop_down", "value"),
)
def country_plot(ycol, country_list):
    yaxis_title = ycol.split("_")
    yaxis_title = " ".join(yaxis_title)
    graph_width = 200
    graph_height = 200
    # Global average line
    global_avg = (
        alt.Chart(test)
        .mark_line()
        .encode(
            x=alt.X("Year:O"),
            y=alt.Y(f"mean({ycol})", scale=alt.Scale(zero=False)),
            color=alt.value("black"),
            opacity=alt.Opacity("Global_Average", legend=alt.Legend(title="")),
        )
        .properties(width=graph_width, height=graph_height)
    )

    # One or more country lines
    country_comparison = (
        alt.Chart(data_cn[data_cn["Country"].isin(country_list)])
        .mark_line()
        .encode(
            x=alt.X("Year:O"),
            y=alt.Y(ycol, scale=alt.Scale(zero=False), title=f"{yaxis_title}"),
            color=alt.Color("Country", title=""),
        )
    )

    # If no countries are selected, only plot the global average
    if len(country_list) == 0:
        return global_avg.to_html()

    # If one or more countries are selected, plot them with the global average
    else:
        chart = (global_avg + country_comparison).properties(
            width=graph_width, height=graph_height
        )
        return chart.to_html()


# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------

# Slider Callbacks
@app.callback(
    Output(component_id="table", component_property="data"),
    Input(
        "slider_health", "value"
    ),  # add more inputs? but then how do you send them to the function?
    Input("slider_free", "value"),
    Input("slider_econ", "value"),
)
def country_list(value_health, value_free, value_econ, data=df):
    data = data.loc[data['Year'] == 2020]
    user_data = [
        ["Life_expectancy", value_health],
        ["Freedom", value_free],
        ["GDP_per_capita", value_econ],
    ]
    country_df = pd.DataFrame(user_data, columns=["Measure", "Value"])
    country_df = country_df.sort_values(by=["Value"], ascending=False)
    col_name = country_df.iloc[0, 0]
    filtered_data = data.sort_values(
        by=[col_name], ascending=False
    )  # filter data somehow (sort by whatever value is most important)

    country_list = filtered_data.iloc[:, 1]
    hr = filtered_data.iloc[:, 2]
#    df_table = pd.DataFrame(country_list[0:5], hr[0:5])

    df_table = pd.DataFrame({'Happiness_rank':hr[0:5],'Country':country_list[0:5]})

    return df_table.to_dict('rows')

#def table_update():


# Reset Button Callback, reset back to 5
@app.callback(
    Output("slider_health", "value"),
    Output("slider_free", "value"),
    Output("slider_econ", "value"),
    [Input("reset_button", "n_clicks")],
)
def update(reset):
    return 5, 5, 5

# # Table callback
# @app.callback(
#     Output(component_id="table", component_property="value"),
#     Input(country_list)
# )
# def update_table(country_list, data=df_2020):
#     return str(country_list[0:5])
# ----------------------------------------------------------------------------------------------

# Map callback
@app.callback(
    Output("map", "srcDoc"),
    Input(
        "slider_health", "value"
    ),  # add more inputs? but then how do you send them to the function?
    Input("slider_free", "value"),
    Input("slider_econ", "value"),
)
def update_map(value_health, value_free, value_econ, data=df):
    map_click = alt.selection_multi(fields=["id"])

    map_chart = (
        alt.Chart(world_map)
        .mark_geoshape(stroke="black", strokeWidth=0.5)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(
                data=df,
                key="id",
                fields=["Country", "Delta_happy", "Happiness_rank"],
            ),
        )
        .encode(
            alt.Color(
                "Delta_happy:Q",
                scale=alt.Scale(domain=[0, 10], scheme="redyellowgreen"),
                legend=alt.Legend(title="Happiness"),
            ),
            opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),
            tooltip=[
                alt.Tooltip(field="Country", type="nominal", title="Country"),
                alt.Tooltip(
                    field="Delta_happy", type="quantitative", title="Happiness"
                ),
                alt.Tooltip(field="Happiness_rank", type="quantitative", title="Rank"),
            ],
        )
        .add_selection(map_click)
        .project(type="naturalEarth1")
        .properties(width=550, height=350)
    )
    return map_chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)