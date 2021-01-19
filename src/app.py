import dash
import dash_html_components as html
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc

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
                dbc.Col(html.H1("Plot1"), md=4),
                dbc.Col(html.H1("Plot2"), md=4),
                dbc.Col(html.H1("Plot3"), md=4),
            ]
        ),
    ]
)
if __name__ == "__main__":
    app.run_server(debug=True)
