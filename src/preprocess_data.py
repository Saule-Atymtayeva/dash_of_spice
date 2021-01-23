"""
Author: Dash-of-Spice

Date: Jan. 22, 2020

Preprocess raw happiness datasets

Usage: preprocess_data.py -i=<input> -o=<output> [-v]

Options:
-i <input>, --input <input>     Local raw data csv file directory
-o <output>, --output <output>  Local output filename and path for preprocessed csv
[-v]                            Report verbose output of dataset retrieval process
"""
import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
from docopt import docopt
args = docopt(__doc__)

def preprocess_data():
    # Starting dataset preprocessing
    print("\n\n##### preprocess_data: Preprocessing datasets")
    if verbose: print(f"Running preprocess_data with arguments: \n {args}")

    # Gather year data csv files
    raw_csv_year_files = glob.glob(f"{input_dir}/20[0-9][0-9].csv")

    # Standardize input columns
    tidy_dfs = []
    for untidy_happiness_csv_file in raw_csv_year_files:
        year = untidy_happiness_csv_file.split(".")[0].split("/")[-1]
        tidy_dfs.append(wrangle_year_df(pd.read_csv(untidy_happiness_csv_file), year))

    # Combine year data csvs
    df_tidy = pd.concat(tidy_dfs, ignore_index=True).round(4)
    if verbose: df_tidy.info()

    # Link countries with topojson countries
    df_tidy = sync_country_names(df_tidy)

    # Saving in a csv file
    df_tidy.to_csv("data/processed/df_tidy.csv", index = False)

    print("\n##### preprocess_data: Finished preprocessing")

def wrangle_year_df(year_df, year):
    # Unfortunately all the year data csvs have different #'s of columns and names...
    drop_columns_list = []
    if year == '2015':
        rename_columns_map = {"Happiness Rank": "Happiness_rank", 
                              "Happiness Score": "Happiness_score",
                              "Economy (GDP per Capita)": "GDP_per_capita", 
                              "Family": "Social_support",
                              "Health (Life Expectancy)": "Life_expectancy",
                              "Trust (Government Corruption)": "Corruption"}
    elif year == '2016':
        drop_columns_list.append([1, 4, 5, 12])
        rename_columns_map = {"Happiness Rank": "Happiness_rank", 
                              "Happiness Score": "Happiness_score",
                              "Economy (GDP per Capita)": "GDP_per_capita", 
                              "Family": "Social_support",
                              "Health (Life Expectancy)": "Life_expectancy",
                              "Trust (Government Corruption)": "Corruption"}
    elif year == '2017':
        drop_columns_list.append([3, 4, 11])
        rename_columns_map = {"Happiness.Rank": "Happiness_rank", 
                              "Happiness.Score": "Happiness_score",
                              "Economy..GDP.per.Capita.": "GDP_per_capita", 
                              "Family": "Social_support",
                              "Health..Life.Expectancy.": "Life_expectancy",
                              "Trust..Government.Corruption.": "Corruption"}
    elif year == '2018':
        rename_columns_map = {"Overall rank": "Happiness_rank", 
                              "Country or region": "Country", 
                              "Score": "Happiness_score",
                              "GDP per capita": "GDP_per_capita", 
                              "Social support": "Social_support",
                              "Healthy life expectancy": "Life_expectancy", 
                              "Freedom to make life choices": "Freedom",
                              "Generosity": "Generosity", 
                              "Perceptions of corruption": "Corruption"}
    elif year == '2019':
        rename_columns_map = {"Overall rank": "Happiness_rank", 
                              "Country or region": "Country", 
                              "Score": "Happiness_score",
                              "GDP per capita": "GDP_per_capita", 
                              "Social support": "Social_support",
                              "Healthy life expectancy": "Life_expectancy", 
                              "Freedom to make life choices": "Freedom",
                              "Generosity": "Generosity", 
                              "Perceptions of corruption": "Corruption"}
    elif year == '2020':
        drop_columns_list.append([1, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19])
        # Adding the `Happiness_rank` column in 2020.csv
        year_df['Happiness_rank'] = range(1, 154)
        rename_columns_map = {"Country name": "Country", 
                              "Ladder score": "Happiness_score",
                              "Logged GDP per capita": "GDP_per_capita", 
                              "Social support": "Social_support",
                              "Healthy life expectancy": "Life_expectancy", 
                              "Freedom to make life choices": "Freedom",
                              "Generosity": "Generosity", 
                              "Perceptions of corruption": "Corruption"}

    else:
        raise Exception(f"Sorry, year value {year} not supported")

    if len(drop_columns_list) > 0:
        # Dropping unnecessary columns
        year_df = year_df.drop(year_df.columns[drop_columns_list], axis=1)

    if rename_columns_map:
        # Renaming the columns
        year_df = year_df.rename(columns=rename_columns_map, errors="raise")

    # Adding the `Year` column to df
    year_df['Year'] = year

    # Standardizing column ordering
    year_df = year_df[['Country', 
                       'Happiness_rank', 
                       'Happiness_score',
                       'GDP_per_capita', 
                       'Social_support', 
                       'Life_expectancy',
                       'Freedom', 
                       'Generosity', 
                       'Corruption', 
                       'Year']]
    if verbose: year_df.info()
    return year_df

def sync_country_names(tidy_df):
    country_ids = pd.read_csv('data/raw/country-ids.csv')

    country_ids = country_ids.append(
    pd.DataFrame([[48,  'Bahrain'],
                  [174, 'Comoros'],
                  [344, 'Hong Kong'],
                  [462, 'Maldives'],
                  [470, 'Malta'],
                  [480, 'Mauritius'],
                  [702, 'Singapore']], columns = ["id", 'name']), ignore_index=True)

    country_mapper = {
        r'^Bolivia.*'              : 'Bolivia',
        r'^Congo$'                 : 'Congo (Kinshasa)',
        r'^Congo.*Demo.*'          : 'Congo (Brazzaville)',
        r'^Cote d.*'               : 'Ivory Coast',
        r'.*Cyprus.*'              : 'Cyprus',
        r'^Hong Kong.*'            : 'Hong Kong',
        r'^Iran.*'                 : 'Iran',
        r'^Korea, R.*'             : 'South Korea',
        r'^Lao.*'                  : 'Laos',
        r'.*Macedonia.*'           : 'North Macedonia',
        r'^Moldova.*'              : 'Moldova',
        r'^Palestinian Territory.*': 'Palestinian Territories',
        r'^Russia.*'               : 'Russia',
        r'^Singapore.*'            : 'Singapore',
        r'^Syria.*'                : 'Syria',
        r'^Somali.*'               : 'Somalia',
        r'^Taiwan.*'               : 'Taiwan',
        r'^Tanzania.*'             : 'Tanzania',
        r'^Trinidad & Tobago'      : 'Trinidad and Tobago',
        r'^Venezuela.*'            : 'Venezuela',
        r'^Viet.*'                 : 'Vietnam'
    }

    tidy_df = tidy_df.replace(regex = country_mapper)
    country_ids = country_ids.replace(regex = country_mapper)
    combined_df = tidy_df.merge(country_ids, left_on = "Country", right_on = 'name')
    combined_df = combined_df.drop(columns = 'name')
    #combined_df['Delta_happy'] = combined_df['Happiness_score']
    return combined_df

def validate_inputs():
    assert os.path.exists(input_dir), "Invalid input directory path provided"
    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    assert os.path.exists(os.path.dirname(output_filename)), "Invalid output path provided"

if __name__ == "__main__":
    input_dir = args["--input"]
    output_filename = args["--output"]
    verbose = args["-v"]
    validate_inputs()
    preprocess_data()
