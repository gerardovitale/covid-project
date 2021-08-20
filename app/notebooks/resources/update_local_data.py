import os
import sys
from shutil import rmtree
from typing import List

import pandas as pd

from config.spark_session import spark


COVID_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


def get_covid_data(url: str = COVID_URL) -> None:
    df = pd.read_csv(url)
    print(f'[INFO] url read -> {url}')
    df.to_csv('data/covid_dataset.csv')
    print('[INFO] data/covid_dataset.csv saved!')


def remove_files(files: List[str]) -> None:
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
            print(f'{file} has been removed')
        elif os.path.isdir(file):
            rmtree(file)
            print(f'{file} has been removed')


def rearrenge_data() -> None:
    df_covid = spark.read.csv('data/covid_dataset.csv', inferSchema=True, header=True)
    try:
        remove_files(['data/covid_dataset.jsonl.gz', 'data/covid_dataset.parquet'])

        df_covid.toJSON().saveAsTextFile('data/covid_dataset.jsonl.gz',
                                         'org.apache.hadoop.io.compress.GzipCodec')
        print('[INFO] jsonl.gz files created: data/covid_dataset.jsonl.gz')

        df_covid.write.parquet('data/covid_dataset.parquet')
        print('[INFO] parquet files created: data/covid_dataset.parquet')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    remove_files(['data/covid_dataset.csv'])
