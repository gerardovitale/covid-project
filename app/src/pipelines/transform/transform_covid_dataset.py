import datetime

import pandas as pd

from config.mongo_config import mongo_client
from resources.time_it import time_it


@time_it
def manage_null_values(covid_data: pd.DataFrame) -> pd.DataFrame:
    covid_data.dropna(subset=['continent'], inplace=True)
    covid_data.loc[covid_data.new_cases.isnull(), 'new_cases'] = 0
    covid_data.loc[covid_data.new_deaths.isnull(), 'new_deaths'] = 0
    covid_data.loc[covid_data.tests_units.isnull(), 'tests_units'] = 'not available'
    return covid_data


@time_it
def add_missing_january_records_mongodb():
    database = mongo_client.get_database('covid-project')
    locations = database.covid_dataset.distinct('location')
    list_to_insert = list()
    for each_loc in locations:
        list_to_insert.append({'location': each_loc,
                               'date': datetime.datetime(year=2020, month=1, day=1),
                               'new_cases': 0,
                               'new_deaths': 0, })
    database.covid_dataset.insert_many(list_to_insert)
