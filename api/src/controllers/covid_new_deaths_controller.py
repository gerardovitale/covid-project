from flask import Blueprint, render_template

from src import DevelopmentConfig
from src.controllers.helpers import add_thousand_separator
from src.services.covid_new_deaths_service import find_covid_new_deaths

covid_new_deaths_bp = Blueprint('covid_new_deaths_bp', __name__)
database = DevelopmentConfig().DATABASE_OBJ


@covid_new_deaths_bp.route('/covid_new_deaths/json/<location>', methods=['GET'])
def get_covid_new_deaths_per_location(location: str):
    location = location.capitalize()
    result = find_covid_new_deaths(database, location)
    result = list(result)
    return {
        'result': result,
        'result_count': result.__len__(),
        'route': f'/covid_new_cases/json/{location}',
        'status': 200,
    }


@covid_new_deaths_bp.route('/covid_new_deaths/table/<location>', methods=['GET'])
def get_covid_new_deaths_per_location_html(location: str):
    location = location.capitalize()
    mongo_data = find_covid_new_deaths(database, location)
    result = add_thousand_separator(mongo_data, 'total_new_deaths')
    return render_template(
        'covid_new_deaths.html',
        output=result,
        location=location
    )


@covid_new_deaths_bp.route('/covid_new_deaths/chart/<location>', methods=['GET'])
def get_covid_new_deaths_chart(location: str):
    location = location.capitalize()
    return render_template(
        'covid_new_deaths_chart.html',
        location=location
    )
