import datetime
from typing import List

from pymongo import DESCENDING
from pymongo.cursor import Cursor
from pymongo.database import Database


def find_vaccination_summary(database: Database, days: int, location: str) -> Cursor:
    to_date = datetime.datetime.today()
    from_date = to_date - datetime.timedelta(days=days)
    query = {'$and': [{'date': {'$gte': from_date,
                                '$lte': to_date}},
                      {'location': location}]}
    project = {
        '_id': 0,
        'date': 1,
        'location': 1,
        'population': 1,
        'new_vaccinations': 1,
        'people_vaccinated': 1,
        'people_fully_vaccinated': 1,
    }
    result = database['covid_dataset'].find(query, project).sort('date', DESCENDING)
    return result


def calculate_vaccination_rate(mongo_data: List):
    """
    AVG(people_vaccinated / population * 100) AS vaccination_rate,
    AVG(people_fully_vaccinated / population * 100) AS fully_vaccination_rate,
    AVG(new_vaccinations / (population - people_fully_vaccinated) * 100) AS new_vaccination_rate
    """
    for doc in mongo_data:
        doc['vaccination_rate'] = doc['people_vaccinated'] / doc['population'] * 100
        doc['fully_vaccination_rate'] = doc['people_fully_vaccinated'] / doc['population'] * 100
        doc['new_vaccination_rate'] = \
            doc['new_vaccinations'] / (doc['population'] - doc['people_fully_vaccinated']) * 100
        yield mongo_data
