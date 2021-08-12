from flask import Flask, render_template, request
from pymongo import MongoClient

from services.covid_summary_service import find_covid_summary
from controllers.helpers import get_query_url_params_covid_summary


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
    location, days = get_query_url_params_covid_summary(request)
    summary = find_covid_summary(database, days, location)
    return {
        'result': summary,
        'route': '/covid_summary',
        'status': 200,
    }


@app.route('/covid_summary', methods=['GET'])
def get_covid_summary_html():
    location, days = get_query_url_params_covid_summary(request)
    summary = find_covid_summary(database, days, location)
    return render_template('covid_summary.html', output=summary)
