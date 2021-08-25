import datetime
import sys
from typing import Dict

import numpy as np
import pandas as pd

from config.mongo_config import MONGODB_URI_COVID, client
from config.spark_session import spark
from pipelines.resources.time_it import time_it
from pipelines.resources.remove_files import remove_files

COVID_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
COVID_FILE_NAME = 'covid_dataset'


@time_it
def get_covid_dataset(strTime_to_dateObject=False) -> pd.DataFrame:
    web_data = pd.read_csv(COVID_URL)
    print(f'[INFO] url read -> {COVID_URL}')

    web_data = web_data[web_data.continent.notnull()]

    mask = web_data.new_cases.isnull()
    web_data.loc[mask, 'new_cases'] = 0

    mask = web_data.new_deaths.isnull()
    web_data.loc[mask, 'new_deaths'] = 0

    mask = web_data.tests_units.isnull()
    web_data.loc[mask, 'tests_units'] = 'not available'

    if strTime_to_dateObject:
        web_data.date = web_data.date.apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    return web_data


@time_it
def save_covid_data(df: pd.DataFrame) -> None:
    spark_df = spark.createDataFrame(df)
    try:
        remove_files([f'data/{COVID_FILE_NAME}.parquet'])
        spark_df.write.parquet(f'data/{COVID_FILE_NAME}.parquet')
        print(f'[INFO] parquet files created: data/{COVID_FILE_NAME}.parquet')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def check_covid_database() -> bool:
    databases = client.list_database_names()
    if 'covid-project' in databases:
        database = client.get_database('covid-project')
        collections = database.list_collection_names()
        if 'covid_dataset' in collections:
            return True
    else:
        return False


def get_last_update_mongodb() -> Dict[str, datetime.datetime]:
    covid_df = spark.read.format("mongo")\
                         .option("uri", MONGODB_URI_COVID)\
                         .load()
    covid_df.createOrReplaceTempView('mongo_covid')
    last_update = spark.sql('''
        SELECT DISTINCT date
        FROM mongo_covid
        ORDER BY 1 DESC
        LIMIT 1
    ''').collect()[0].asDict()
    return last_update


def get_new_records_from_web_data(df: pd.DataFrame, last_update: datetime.datetime) -> pd.DataFrame:
    mask = (df.date > last_update.strftime('%Y-%m-%d'))
    return df.loc[mask]
