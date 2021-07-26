from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
database = MongoClient(host='mongodb://mongo_db', 
                       port=27017)\
                           .get_database('covid-project')


@app.route('/', methods=['GET'])
def home():
    return {
        'result': {
            'api': 'covid-api',
            'documentation': '<isert_url>',
            'endpoints': [
                '/',
                '/covid_deaths',
            ],
        },
        'route': '/',
        'status': 200,
    }


@app.route('/covid_deaths', methods=['GET'])
def get_covid_deaths_per_months():
    location = request.args.get('location')
    date = request.args.get('date')
    query = {'location': location, 'date': date}
    project = {'country': 1, 'date': 1, 'new_deaths': 1}
    new_deaths = list(database['covid_deaths'].find(query, project))
    print(location,new_deaths)
    return {
        'result': {
            'location': location,
            'date': date,
            'new_deaths': new_deaths
        },
        'route': '/covid_deaths',
        'status': 200,
    }