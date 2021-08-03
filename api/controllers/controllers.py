from flask import Flask, render_template, request
from pymongo import MongoClient

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
def get_covid_summary_per_date_as_html():
    location = request.args.get('location').capitalize()
    date = request.args.get('date')
    query = {'location': location, 'date': date}
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
    for element in result:
        element['infected_rate'] = element['total_cases'] / element['population'] * 100
        element['death_rate'] = element['total_deaths'] / element['total_cases'] * 100
    return {
        'result': result,
        'route': '/covid_summary',
        'status': 200,
    }


@app.route('/covid_summary', methods=['GET'])
def get_covid_summary_per_date():
    location = request.args.get('location').capitalize()
    date = request.args.get('date')
    query = {'location': location, 'date': date}
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
        row['infected_rate'] = round(row['total_cases'] / row['population'] * 100, 3)
        row['death_rate'] = round(row['total_deaths'] / row['total_cases'] * 100, 3)
    return render_template('covid_summary.html', output=result)
