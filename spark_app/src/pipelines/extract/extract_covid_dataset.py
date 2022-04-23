import pandas as pd

from src.resources.time_it import time_it

COVID_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


@time_it
def get_covid_dataset() -> pd.DataFrame:
    """Get covid dataset from COVID_URL as a panda DataFrame"""
    web_data = pd.read_csv(COVID_URL)
    print(f'[INFO] url read -> {COVID_URL}')
    return web_data
