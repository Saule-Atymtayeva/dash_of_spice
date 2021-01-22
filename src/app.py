import dash
import dash_html_components as html
import dash_table
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


data_cn = pd.read_csv("../data/processed/cn_tidy.csv")
test = data_cn
test["Global_Average"] = "Global Average"

unique_countries = data_cn["Country"].unique()
country_options = [{"label": c, "value": c} for c in unique_countries]

# for table
df = pd.read_csv("../data/processed/df_tidy.csv")
df_2020 = df.loc[df['Year'] == 2020]

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

# Import happiness dataset (2020 for now)
happiness_df = pd.read_csv("../data/processed/extra_clean.csv")
world_map = alt.topo_feature(data.world_110m.url, "countries")
# happiness_df = pd.DataFrame(happiness_data)


# ----------------------------------------------------------------------------------------------

# Slider Callbacks
@app.callback(
    Output(component_id="list_text", component_property="value"),
    Input(
        "slider_health", "value"
    ),  # add more inputs? but then how do you send them to the function?
    Input("slider_free", "value"),
    Input("slider_econ", "value"),
)
def country_list(value_health, value_free, value_econ, data=happiness_df):
    data = [
        ["Healthy life expectancy", value_health],
        ["Freedom to make life choices", value_free],
        ["Logged GDP per capita", value_econ],
    ]
    country_df = pd.DataFrame(data, columns=["Measure", "Value"])
    country_df = country_df.sort_values(by=["Value"], ascending=False)
    col_name = country_df.iloc[0, 0]
    filtered_data = happiness_df.sort_values(
        by=[col_name]
    )  # filter data somehow (sort by whatever value is most important)

    country_list = filtered_data.iloc[:, 0]
    return str(country_list[0:5])


# Reset Button Callback, reset back to 5
@app.callback(
    Output("slider_health", "value"),
    Output("slider_free", "value"),
    Output("slider_econ", "value"),
    [Input("reset_button", "n_clicks")],
)
def update(reset):
    return 5, 5, 5


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
def update_map(value_health, value_free, value_econ, data=happiness_df):
    map_click = alt.selection_multi(fields=["id"])

    map_chart = (
        alt.Chart(world_map)
        .mark_geoshape(stroke="black", strokeWidth=0.5)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(
                data=happiness_df,
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
