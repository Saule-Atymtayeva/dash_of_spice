# Dash-of-Spice: Happiness Navigator
## App Description

The Happiness Navigator app dashboard is an interactive visual tool to help users navigate, filter, and compare the [results](https://www.kaggle.com/mathurinache/world-happiness-report) of the [World Happiness Report](https://en.wikipedia.org/wiki/World_Happiness_Report). The report is a survey of citizens from each of the 153 participating countries that attempts to quantify their overall happiness and quality of life over a range of metrics, and then combines this information into a single happiness score.

The main visual focus of the app is a navigable world map, that if no countries are selected uses a sequential color gradient and legend to indicate the happiness scores of each nation given the currently metric weights. If countries are selected by clicking or using the text input search dropdown, they are highlighted in different colours mapped by the legend. These results are summarized in the right panel with a scrollable list of all or selected countries sorted by score.

The collapsible user input panel on the left contains input sliders and dropdowns to weight each of the quality of life metrics between 0 and 100 to customize and update the combined happiness score relative to the users preferences. This panel also contains a year range selector to filter from which years to use survey data to see how scores are changing over time, or to limit data to only the most recent. Finally, this panel also includes reset button to restore all sliders and app inputs back to a fresh state.

On the bottom of the dashboard are a row of distribution plots for each quality of life metric. If no countries are selected, these will display density plots of each metric and annotations of key global parameters. If the user selects countries, these plots will transform to directly compare metrics between selections and global averages with bar charts.

## App Sketch

The initial dashboard showing the top 5 countries based on the user's ranking inputs:
![Initial Dashboard](sketch/dos_sketch_a.png)

>

The final dashboard showing the rankings of the rest of the countries and the bottom 5 countries after scrolling. Clicking on another country will highlight it with the top country, and clicking the arrows in the plots section will display different feature ranks.
![Final Dashboard](sketch/dos_sketch_b.png)