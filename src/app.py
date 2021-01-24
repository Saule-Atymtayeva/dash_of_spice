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

data_country_plots = pd.read_csv("data/processed/df_tidy.csv")
data_country_plots["Global_Average"] = "Global Average"

unique_countries = data_country_plots["Country"].unique()
country_options = [{"label": c, "value": c} for c in unique_countries]

# for table
df = pd.read_csv("data/processed/df_tidy.csv")
df["Delta_happy"] = df["Happiness_score"]
df_2020 = df.loc[df["Year"] == 2020]
world_map = alt.topo_feature(data.world_110m.url, "countries")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server  # for heroku

# ----------------------------------------------------------------------------------------------

# Images
image_filename = "assets/logo.png"
encoded_image = base64.b64encode(open(image_filename, "rb").read())
image_filename2 = "assets/smiley.gif"
encoded_image2 = base64.b64encode(open(image_filename2, "rb").read())
app.layout = dbc.Container(
    [
        html.H1(),
        # Top screen (logo, years, smiley face)
        dbc.Row(
            [
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'60%', 'width':'20%'}), md=4),
                dbc.Col(html.H1("The Happiness Navigator"), md=6),
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'align': 'end', 'justify': 'end', 'height':'60%', 'width':'20%'}), md=2),
            ]
        ),
        dbc.Row(
            [
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
                                    "verticalAlign": "middle",
                                    "border-width": "10",
                                    "width": "100%",
                                    "height": "20px",
                                    "margin": "10px",
                                },
                            ),
                        ]
                    ),
                    width={"size": 6, "offset": 4},
                )
            ]
        ),
        # Main screen layout
        dbc.Row(
            [
                dbc.Col(
                    # slider = dbc.FormGroup(
                    [
                        html.H2("Happiness Metrics:"),
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
                        html.Button("Reset", id="reset_button", n_clicks=0,              
                                style={
                                    "backgroundColor": '#FFFF00',
                                    'horizonalAlign': 'center',
                                    "verticalAlign": "center",
                                    "border-width": "10",
                                    "width": "80%",
                                    "height": "40px",
                                    "margin": "10px",
                                },),
                        html.Br(),
                        html.Br(),
                        html.Label(
                            [
                                "Choose your happiness navigator!",
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
                                        "margin": "10px",
                                    },
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="country_plot",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "600px",
                            },
                        )
                    ],
                    md=6,
                ),
                dbc.Col(html.Div([html.H3('Top 10 Countries'),
                                  dash_table.DataTable(id = 'top_5_table', 
                                                       style_cell={'backgroundColor':'#FFFF00',
                                                                   'textAlign' : 'center'})
                    ]),
                                width={'size': 3,  "offset": 0, 'order': 3}
                ),
            ]
        ),
    ]
)

# Slider Callbacks
@app.callback(
    Output('top_5_table', 'data'),
    Output('top_5_table', 'columns'),
    Input(
        "slider_health", "value"
    ),  # add more inputs? but then how do you send them to the function?
    Input("slider_free", "value"),
    Input("slider_econ", "value"),
)
def country_list(value_health, value_free, value_econ, data=df):
    data = data.loc[data["Year"] == 2020]
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

    country_list = filtered_data.iloc[:, 0]
    hr = filtered_data.iloc[:, 1]
#    df_table = pd.DataFrame(country_list[0:5], hr[0:5])

    df_table = pd.DataFrame({'Rank' : hr[0:10],
                             'Country' : country_list[0:10]})

    cols = [{'name': i, 'id': i} for i in df_table.columns]
    data = df_table.to_dict('rows')

    return data, cols #df_table.to_dict('rows')

    return df_table.to_dict("rows")


# Reset Button Callback, reset back to 5
@app.callback(
    Output("slider_health", "value"),
    Output("slider_free", "value"),
    Output("slider_econ", "value"),
    [Input("reset_button", "n_clicks")],
)
def update(reset):
    return 5, 5, 5


# Link and plot the map and country plot
@app.callback(
    Output("country_plot", "srcDoc"),
    Input("yaxis_feature", "value"),
    Input("country_drop_down", "value"),
    Input(
        "slider_health", "value"
    ),  # add more inputs? but then how do you send them to the function?
    Input("slider_free", "value"),
    Input("slider_econ", "value"),
)
def country_plot(ycol, country_list, value_health, value_free, value_econ, data=df):

    data_sliders = data.loc[data["Year"] == 2020]
    user_data = [
        ["Life_expectancy", value_health],
        ["Freedom", value_free],
        ["GDP_per_capita", value_econ],
    ]
    country_df = pd.DataFrame(user_data, columns=["Measure", "Value"])
    country_df = country_df.sort_values(by=["Value"], ascending=False)
    col_name = country_df.iloc[0, 0]
    filtered_data = data_sliders.sort_values(
        by=[col_name], ascending=False
    )  # filter data somehow (sort by whatever value is most important)

    country_selections = filtered_data.iloc[:, 0]
    country_selections = country_selections[0:5]

    # Create the map object
    presets = [
        {"id": value}
        for value in data[data["Country"].isin(country_selections)]["id"].unique()
    ]
    map_click = alt.selection_multi(fields=["id"], init=presets)

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
        .properties(width=400, height=300)
    )

    # Create the plot objects
    print(ycol)
    yaxis_title = ycol.split("_")
    yaxis_title = " ".join(yaxis_title)
    graph_width = 350
    graph_height = 200

    # One or more country lines
    country_comparison_from_map = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X("Year:O"),
            y=alt.Y(ycol, scale=alt.Scale(zero=False), title=f"{yaxis_title}"),
            color=alt.Color("Country", title=""),
        )
        .transform_filter(map_click)
        .properties(width=graph_width, height=graph_height)
    )

    # This will plot the searched countries regardless of what is clicked on the map
    country_comparison_from_search = (
        alt.Chart(data_country_plots[data_country_plots["Country"].isin(country_list)])
        .mark_line()
        .encode(
            x=alt.X("Year:O"),
            y=alt.Y(ycol, scale=alt.Scale(zero=False), title=f"{yaxis_title}"),
            color=alt.Color("Country", title=""),
        )
        .properties(width=graph_width, height=graph_height)
    )

    # If no countries are selected, only plot the global average
    if len(country_list) == 0:
        return ((map_chart).configure_view(strokeOpacity=0)).to_html()

    # If one or more countries are selected, plot them with the global average
    else:
        return (
            (map_chart & (country_comparison_from_map + country_comparison_from_search)).configure_view(strokeOpacity=0)
        ).to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
