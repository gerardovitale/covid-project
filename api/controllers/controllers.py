from flask import Flask, render_template, request
from pymongo import MongoClient

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
def get_covid_deaths_summary_per_date():
    location = request.args.get('location')
    date = request.args.get('date')
    query = {'location': location, 'date': date}
    project = {'_id':0, 
               'location': 1, 
               'date': 1, 
               'new_deaths': 1,
               'new_cases':1,}
    result = list(database['covid_deaths'].find(query, project))[0]
    return {
        'result': result,
        'route': '/covid_deaths',
        'status': 200,
    }