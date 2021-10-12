import datetime

import pandas as pd

from config.mongo_config import mongo_client
from pipelines.resources.time_it import time_it

COVID_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
COVID_FILE_NAME = 'covid_dataset'


@time_it
def manage_null_values(covid_data: pd.DataFrame) -> pd.DataFrame:
    # remove records when continent is null
    covid_data = covid_data[covid_data.continent.notnull()]
    #
    mask = covid_data.new_cases.isnull()
    covid_data.loc[mask, 'new_cases'] = 0

    mask = covid_data.new_deaths.isnull()
    covid_data.loc[mask, 'new_deaths'] = 0

    mask = covid_data.tests_units.isnull()
    covid_data.loc[mask, 'tests_units'] = 'not available'

    return covid_data


@time_it
def add_missing_january_records_mongodb():
    database = mongo_client.get_database('covid-project')
    locations = database.covid_dataset.distinct('location')
    list_to_insert = list()
    for each_loc in locations:
        list_to_insert.append({'location': each_loc,
                               'date': datetime.datetime(year=2020, month=1, day=1),
                               'new_cases': 0.0,
                               'new_deaths': 0.0, })
    database.covid_dataset.insert_many(list_to_insert)