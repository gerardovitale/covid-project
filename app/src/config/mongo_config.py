from pymongo import MongoClient

MONGODB_HOST = "mongodb://mongo_db:27017"
MONGODB_URI = f"{MONGODB_HOST}/covid-project"
MONGODB_URI_COVID = f"{MONGODB_URI}.covid_dataset"
MONGODB_URI_NEW_CASES_CHART_DATA = f"{MONGODB_URI}.total_new_cases_chart_data"

mongo_client = MongoClient(f"{MONGODB_HOST}")
