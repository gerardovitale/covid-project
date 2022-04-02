from flask import Blueprint, render_template

from src import DevelopmentConfig
from src.controllers.helpers import add_thousand_separator
from src.services.covid_new_cases_service import find_covid_new_cases

covid_new_cases_bp = Blueprint('covid_new_cases_bp', __name__)
database = DevelopmentConfig().DATABASE_OBJ


@covid_new_cases_bp.route('/covid_new_cases/json/<location>', methods=['GET'])
def get_covid_new_cases_per_location(location: str):
    location = location.capitalize()
    result = find_covid_new_cases(database, location)
    result = list(result)
    return {
        'result': result,
        'result_count': result.__len__(),
        'route': f'/covid_new_cases/json/{location}',
        'status': 200,
    }


@covid_new_cases_bp.route('/covid_new_cases/table/<location>', methods=['GET'])
def get_covid_new_cases_per_location_html(location: str):
    location = location.capitalize()
    mongo_data = find_covid_new_cases(database, location)
    result = add_thousand_separator(mongo_data, 'total_new_cases')
    return render_template(
        'covid_new_cases.html',
        output=result,
        location=location
    )


@covid_new_cases_bp.route('/covid_new_cases/chart/<location>', methods=['GET'])
def get_covid_new_cases_chart(location: str):
    location = location.capitalize()
    return render_template(
        'covid_new_cases_chart.html',
        location=location
    )
