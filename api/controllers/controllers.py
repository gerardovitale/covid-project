import datetime

from flask import Flask, render_template, request
from pymongo import MongoClient

from services.covid_summary_service import find_covid_data
from controllers.helpers import get_url_query_params

app = Flask(__name__, template_folder='templates')
database = MongoClient(host='mongodb://mongo_db:27017')\
            .get_database('covid-project')


@app.route('/', methods=['GET'])
def home():
    return {
        'result': {
            'api': 'covid-api',
            'documentation': '<isert_url>',
            'endpoints': [
                '/',
                '/covid_summary',
            ],
        },
        'route': '/',
        'status': 200,
    }


@app.route('/covid_summary.json', methods=['GET'])
def get_covid_summary():
    location, days = get_url_query_params(request)
    summary = find_covid_data(database, days, location)
    return {
        'result': summary,
        'route': '/covid_summary',
        'status': 200,
    }


@app.route('/covid_summary', methods=['GET'])
def get_covid_summary_html():
    location, days = get_url_query_params(request)
    summary = find_covid_data(database, days, location)
    return render_template('covid_summary.html', output=summary)
