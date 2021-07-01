import pandas as pd


CSV_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'


def get_covid_data(url: str = CSV_URL) -> None:
    df = pd.read_csv(url)
    print(f'[INFO] url read -> {url}')
    split_1 = df.iloc[:,0:25]
    split_2 = df.iloc[:,25:]
    split_1['population'] = split_2['population']
    split_1.to_csv('../data/covid_deaths.csv')
    print('[INFO] data/covid_deaths.csv saved')
    split_2.to_csv('../data/covid_vaccinations.csv')
    print('[INFO] data/covid_vaccinations.csv saved')
