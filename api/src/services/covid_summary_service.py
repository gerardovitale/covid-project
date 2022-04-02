import datetime
from typing import Any, Dict, List

from pymongo import DESCENDING
from pymongo.cursor import Cursor
from pymongo.database import Database


def find_covid_summary(database: Database, days: int, location: str) -> Cursor:
    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=days)
    query = {'$and': [{'date': {'$gte': from_date,
                                '$lte': to_date}},
                      {'location': location}]}
    project = {'_id': 0,
               'date': 1,
               'location': 1,
               'population': 1,
               'new_deaths': 1,
               'new_cases': 1,
               'icu_patients': 1,
               'hosp_patients': 1,
               'total_cases': 1,
               'total_deaths': 1}
    result = database['covid_dataset'].find(query, project).sort('date', DESCENDING)
    return result


def paginate_mongo_data(mongo_data: Cursor, start: int, width: int) -> Cursor:
    return mongo_data.skip(start).limit(width)


def calculate_rates(mongo_data: Cursor) -> List[Dict[str, Any]]:
    mongo_data = list(mongo_data)
    for doc in mongo_data:
        doc['infected_rate'] = doc['total_cases'] / doc['population'] * 100
        doc['death_rate'] = doc['total_deaths'] / doc['total_cases'] * 100
    return mongo_data
