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


@app.route('/covid_new_deaths/table/<location>', methods=['GET'])
def get_covid_new_deaths_per_location_html(location: str):
    location = location.capitalize()
    result = find_covid_new_deaths(database, location)
    return render_template(
        'covid_new_deaths.html',
        output=list(result),
        location=location
    )


@app.route('/covid_new_deaths/chart/<location>', methods=['GET'])
def get_covid_new_deaths_chart(location: str):
    location = location.capitalize()
    return render_template(
        'covid_new_deaths_chart.html',
        location=location
    )
