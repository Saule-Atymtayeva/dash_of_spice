"""
Author: <>

Date: <>

Preprocess raw datasets

Usage: preprocess_data.py

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
#from docopt import docopt
#args = docopt(__doc__)


def preprocess_data():
    # Reading the data from csv for 2020
    df_2020_untidy = pd.read_csv("../data/raw/2020.csv")
    df_2020_untidy.head()

    # Dropping unnecessary columns in 2020.csv
    df_2020_tidy = df_2020_untidy.drop(df_2020_untidy.columns[[1, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19]], axis=1)

    # Adding the `Happiness_rank` column in 2020.csv
    df_2020_tidy.insert(0, 'Happiness_rank', range(1, 154))

    # Adding the `Year` column in 2020.csv
    df_2020_tidy.insert(0, 'Year', '2020')

    # Renaming the columns in 2020.csv
    df_2020_tidy = df_2020_tidy.rename(columns={"Country name": "Country", "Ladder score": "Happiness_score",
                                  "Logged GDP per capita": "GDP_per_capita", "Social support": "Social_support",
                                  "Healthy life expectancy": "Life_expectancy", "Freedom to make life choices": "Freedom",
                                  "Generosity": "Generosity", "Perceptions of corruption": "Corruption"}, errors="raise")

    # Reordering the columns in 2020.csv
    df_2020_tidy = df_2020_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                                 'GDP_per_capita', 'Social_support', 'Life_expectancy',
                                 'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2020_tidy.info()

    # Reading the data from csv for 2019
    df_2019_untidy = pd.read_csv("../data/raw/2019.csv")
    df_2019_untidy.head()

    # Adding the `Year` column in 2019.csv
    df_2019_untidy.insert(0, 'Year', '2019')

    # Renaming the columns in 2019.csv
    df_2019_tidy = df_2019_untidy.rename(columns={"Overall rank": "Happiness_rank", "Country or region": "Country", "Score": "Happiness_score",
                                                  "GDP per capita": "GDP_per_capita", "Social support": "Social_support",
                                                  "Healthy life expectancy": "Life_expectancy", "Freedom to make life choices": "Freedom",
                                                  "Generosity": "Generosity", "Perceptions of corruption": "Corruption"}, errors="raise")

    # Reordering the columns in 2019.csv
    df_2019_tidy = df_2019_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                                 'GDP_per_capita', 'Social_support', 'Life_expectancy',
                                 'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2019_tidy.info()

    # Reading the data from csv for 2018
    df_2018_untidy = pd.read_csv("../data/raw/2018.csv")
    df_2018_untidy.head()

    # Adding the `Year` column in 2018.csv
    df_2018_untidy.insert(0, 'Year', '2018')

    # Renaming the columns in 2018.csv
    df_2018_tidy = df_2018_untidy.rename(columns={"Overall rank": "Happiness_rank", "Country or region": "Country", "Score": "Happiness_score",
                                  "GDP per capita": "GDP_per_capita", "Social support": "Social_support",
                                  "Healthy life expectancy": "Life_expectancy", "Freedom to make life choices": "Freedom",
                                  "Generosity": "Generosity", "Perceptions of corruption": "Corruption"}, errors="raise")

    # Reordering the columns in 2018.csv
    df_2018_tidy = df_2018_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                                 'GDP_per_capita', 'Social_support', 'Life_expectancy',
                                 'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2018_tidy.info()

    # Reading the data from csv for 2017
    df_2017_untidy = pd.read_csv("../data/raw/2017.csv")
    df_2017_untidy.head()

    # Dropping unnecessary columns in 2017.csv
    df_2017_tidy = df_2017_untidy.drop(df_2017_untidy.columns[[3, 4, 11]], axis=1)

    # Adding the `Year` column in 2017.csv
    df_2017_tidy.insert(0, 'Year', '2017')

    # Renaming the columns in 2017.csv
    df_2017_tidy = df_2017_tidy.rename(columns={"Happiness.Rank": "Happiness_rank", "Happiness.Score": "Happiness_score",
                                  "Economy..GDP.per.Capita.": "GDP_per_capita", "Family": "Social_support",
                                  "Health..Life.Expectancy.": "Life_expectancy",
                                  "Trust..Government.Corruption.": "Corruption"}, errors="raise")

    # Reordering the columns in 2017.csv
    df_2017_tidy = df_2017_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                            'GDP_per_capita', 'Social_support', 'Life_expectancy',
                            'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2017_tidy.info()

    # Reading the data from csv for 2016
    df_2016_untidy = pd.read_csv("../data/raw/2016.csv")
    df_2016_untidy.head()

    # Dropping unnecessary columns in 2016.csv
    df_2016_tidy = df_2016_untidy.drop(df_2016_untidy.columns[[1, 4, 5, 12]], axis=1)

    # Adding the `Year` column in 2016.csv
    df_2016_tidy.insert(0, 'Year', '2016')

    # Renaming the columns in 2017.csv
    df_2016_tidy = df_2016_tidy.rename(columns={"Happiness Rank": "Happiness_rank", "Happiness Score": "Happiness_score",
                                                "Economy (GDP per Capita)": "GDP_per_capita", "Family": "Social_support",
                                                "Health (Life Expectancy)": "Life_expectancy",
                                                "Trust (Government Corruption)": "Corruption"}, errors="raise")

    # Reordering the columns in 2017.csv
    df_2016_tidy = df_2016_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                                 'GDP_per_capita', 'Social_support', 'Life_expectancy',
                                 'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2016_tidy.info()

    # Reading the data from csv for 2015
    df_2015_untidy = pd.read_csv("../data/raw/2015.csv")
    df_2015_untidy.head()

    # Adding the `Year` column in 2015.csv
    df_2015_untidy.insert(0, 'Year', '2015')

    # Renaming the columns in 2017.csv
    df_2015_tidy = df_2015_untidy.rename(columns={"Happiness Rank": "Happiness_rank", "Happiness Score": "Happiness_score",
                                                  "Economy (GDP per Capita)": "GDP_per_capita", "Family": "Social_support",
                                                  "Health (Life Expectancy)": "Life_expectancy",
                                                  "Trust (Government Corruption)": "Corruption"}, errors="raise")

    # Reordering the columns in 2017.csv
    df_2015_tidy = df_2015_tidy[['Country', 'Happiness_rank', 'Happiness_score',
                                 'GDP_per_capita', 'Social_support', 'Life_expectancy',
                                 'Freedom', 'Generosity', 'Corruption', 'Year']]
    df_2015_tidy.info()

    # Concatenating all dataframes
    dfs = [df_2015_tidy, df_2016_tidy, df_2017_tidy, df_2018_tidy, df_2019_tidy, df_2020_tidy]
    df_tidy = pd.concat(dfs, ignore_index=True)
    df_tidy[['Happiness_score', 'GDP_per_capita',
             'Social_support', 'Life_expectancy',
             'Freedom', 'Generosity', 'Corruption']] =  df_tidy[['Happiness_score', 'GDP_per_capita',
                                                                      'Social_support', 'Life_expectancy',
                                                                      'Freedom', 'Generosity', 'Corruption']].round(4)
    df_tidy

    # Saving in a csv file
    df_tidy.to_csv("../data/processed/df_tidy.csv")

if __name__ == "__main__":
    #input_dir = args["--input"]
    #output_filename = args["--output"]
    #verbose = args["-v"]
    preprocess_data()
