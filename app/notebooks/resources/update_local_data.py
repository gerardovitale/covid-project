import os
import sys
from shutil import rmtree
from typing import List

import pandas as pd

from config.spark_session import spark

COVID_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DENSI_URL = 'https://worldpopulationreview.com/dbebbb3f-8d0e-473c-86f2-ca5640e8e307'
FILES_TO_REMOVE = ['data/covid_deaths.jsonl.gz', 'data/covid_vaccinations.jsonl.gz', 
                   'data/world_population_density.jsonl.gz', 'data/gdp_evol_per_country.jsonl.gz',
                   'data/covid_deaths.parquet', 'data/covid_vaccinations.parquet', 
                   'data/world_population_density.parquet', 'data/gdp_evol_per_country.parquet']


def get_covid_data(url: str = COVID_URL) -> None:
    df = pd.read_csv(url)
    print(f'[INFO] url read -> {url}')
    split_1 = df.iloc[:,0:25]
    split_2 = df.iloc[:,25:]
    split_1['population'] = split_2['population']
    split_1.to_csv('data/covid_deaths.csv')
    print('[INFO] data/covid_deaths.csv saved')
    split_2.to_csv('data/covid_vaccinations.csv')
    print('[INFO] data/covid_vaccinations.csv saved')


def remove_files(files: List[str]) -> None:
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            rmtree(file)


def rearrenge_data() -> None:
    df_deaths = spark.read.csv('data/covid_deaths.csv', inferSchema=True, header=True)
    df_vaccination = spark.read.csv('data/covid_vaccinations.csv', inferSchema=True, header=True)
    df_pop_density = spark.read.csv('data/world_population_density.csv', inferSchema=True, header=True)
    # df_gdp = spark.read.csv('data/gdp_evol_per_country.csv', inferSchema=True, header=True)
    try:
        remove_files(FILES_TO_REMOVE)
        df_deaths.toJSON().saveAsTextFile('data/covid_deaths.jsonl.gz', 
                                          'org.apache.hadoop.io.compress.GzipCodec')
        df_vaccination.toJSON().saveAsTextFile('data/covid_vaccinations.jsonl.gz', 
                                               'org.apache.hadoop.io.compress.GzipCodec')
        df_pop_density.toJSON().saveAsTextFile('data/world_population_density.jsonl.gz',
                                               'org.apache.hadoop.io.compress.GzipCodec')
        # df_gdp.toJSON().saveAsTextFile('data/gdp_per_country.jsonl.gz',
        #                                'org.apache.hadoop.io.compress.GzipCodec')
        print('''[INFO] jsonl.gz files created:
        data/covid_deaths.jsonl.gz
        data/covid_vaccinations.jsonl.gz
        data/world_population_density.jsonl.gz''')
        df_deaths.write.parquet('data/covid_deaths.parquet')
        df_vaccination.write.parquet('data/covid_vaccinations.parquet')
        df_pop_density.write.parquet('data/world_population_density.parquet')
        # df_gdp.write.parquet('data/gdp_per_country.parquet')
        print('''[INFO] parquet files created: 
        data/covid_deaths.parquet
        data/covid_vaccinations.parquet
        data/world_population_density.parquet''')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    remove_files(['data/covid_deaths.csv', 'data/covid_vaccinations.csv'])
