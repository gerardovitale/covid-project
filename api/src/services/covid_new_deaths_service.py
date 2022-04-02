from pymongo import ASCENDING
from pymongo.cursor import Cursor
from pymongo.database import Database


def find_covid_new_deaths(database: Database, location: str) -> Cursor:
    query = {'location': location}
    project = {'_id': 0,
               'year': 1,
               'month': 1,
               'location': 1,
               'total_new_deaths': 1}
    result = database['total_new_deaths_chart_data'] \
        .find(query, project) \
        .sort([('year', ASCENDING), ('month', ASCENDING)])
    return result
