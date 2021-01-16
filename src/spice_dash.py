import dash
import dash_html_components as html
import folium
import altair as alt
from vega_datasets import data
import pandas as pd

df_2020 = pd.read_csv("../data/raw/2020.csv")
df_2020 = df_2020.rename(columns = {'Country name': 'name',
                                    'Ladder score': 'score'})
df_2020 = df_2020[['name', 'score']]
df_2020.loc[df_2020.name == 'United States', 'name'] = 'United States of America'

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
)
world_geo = f"{url}/world-countries.json"

m = folium.Map(zoom_start=3)

folium.Choropleth(
    geo_data=world_geo,
    name="choropleth",
    data=df_2020,
    columns=["name", "score"],
    key_on="feature.properties.name",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Happiness Rating (0 - 10)",
).add_to(m)

folium.LayerControl().add_to(m)

app = dash.Dash(__name__)

app.layout = html.Div([
        html.Iframe(srcDoc=m.get_root().render(),
        style={'border-width': '0', 'width': '600px', 'height': '600px'})])

if __name__ == '__main__':
    app.run_server(debug=True)