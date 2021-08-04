import datetime
from typing import Any, Dict

from pymongo import MongoClient


def find_covid_data(database: MongoClient, days: int, location: str) -> Dict[str, Any]:
    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=days)
    query = {'$and': [{'date': {'$gte': from_date,
                                '$lte': to_date}},
                      {'location': location}]}
    project = {'_id':0,
               'date': 1,
               'location': 1,
               'population':1,
               'new_deaths': 1,
               'new_cases':1,
               'icu_patients':1,
               'hosp_patients':1,
               'total_cases':1,
               'total_deaths':1}
    result = list(database['covid_deaths'].find(query, project))
    for row in result:
        row['infected_rate'] = row['total_cases'] / row['population'] * 100
        row['death_rate'] = row['total_deaths'] / row['total_cases'] * 100
    return result