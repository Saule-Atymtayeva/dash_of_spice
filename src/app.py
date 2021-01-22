import dash
import dash_html_components as html
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

country_clicked = "Canada"
data = pd.read_csv("df_tidy.csv")
test = data
test["Global_Average"] = "Global Average"

unique_countries = data["Country"].unique()
country_options = [{"label": c, "value": c} for c in unique_countries]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
                dbc.Col(html.H1("Sliders"), md=3),
                dbc.Col(html.H1("Map"), md=6),
                dbc.Col(html.H1("Top Countries List"), md=3),
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
                    ]
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
                    )
                ),
                dbc.Col(
                    html.Iframe(
                        id="country_plot",
                        style={
                            "border-width": "0",
                            "width": "400px",
                            "height": "400px",
                        },
                    )
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
        alt.Chart(data[data["Country"].isin(country_list)])
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


if __name__ == "__main__":
    app.run_server(debug=True)
