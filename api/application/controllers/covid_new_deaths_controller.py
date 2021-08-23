from flask import render_template

from application import app, database

from application.services.covid_new_deaths_service import find_covid_new_deaths


@app.route('/covid_new_deaths/json/<location>', methods=['GET'])
def get_covid_new_deaths_per_location(location: str):
    location = location.capitalize()
    result = find_covid_new_deaths(database, location)
    record_count = result.count()
    return {
        'result': list(result),
        'result_count': record_count,
        'route': f'/covid_new_cases/json/{location}',
        'status': 200,
    }
