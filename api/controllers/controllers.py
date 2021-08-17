from flask import Flask, render_template, request
from pymongo import MongoClient

from services.covid_summary_service import (find_covid_summary, 
                                            calculate_rates, 
                                            paginate_mongo_data)
from services.covid_new_cases_service import find_covid_new_cases
from controllers.helpers import (get_params_covid_summary, 
                                 get_params_pagination)


template_folder = '../views/templates'
app = Flask(__name__, template_folder=template_folder)
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
                '/covid_new_cases/<location>',
            ],
        },
        'route': '/',
        'status': 200,
    }


@app.route('/covid_summary.json', methods=['GET'])
def get_covid_summary():
    location, days = get_params_covid_summary(request)
    summary = find_covid_summary(database, days, location)
    return {
        'result': summary,
        'route': '/covid_summary',
        'status': 200,
    }


@app.route('/covid_summary', methods=['GET'])
def get_covid_summary_html():
    location, days = get_params_covid_summary(request)
    start, width, nav_offsets = get_params_pagination(request)
    summary = find_covid_summary(database, days, location)
    summary = paginate_mongo_data(summary, start, width)
    record_count = summary.count()
    summary = calculate_rates(summary)
    return render_template(
        'covid_summary.html',
        output=summary,
        location=location,
        days=days,
        record_count=record_count,
        nav_path=request.path,
        nav_offsets=nav_offsets
    )


@app.route('/covid_new_cases.json/<location>', methods=['GET'])
def get_covid_new_cases_per_location(location: str):
    location = location.capitalize()
    result = find_covid_new_cases(database, location)
    return {
        'result': list(result),
        'route': f'/covid_new_cases/{location}',
        'status': 200,
    }


@app.route('/covid_new_cases/<location>', methods=['GET'])
def get_covid_new_cases_per_location_html(location: str):
    location = location.capitalize()
    result = find_covid_new_cases(database, location)
    return render_template(
        'covid_new_cases.html',
        output=list(result),
        location=location
    )
