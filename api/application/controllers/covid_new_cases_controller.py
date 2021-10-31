from flask import Blueprint, render_template

from application import DevelopmentConfig
from application.services.covid_new_cases_service import find_covid_new_cases

covid_new_cases_bp = Blueprint('covid_new_cases_bp', __name__)
database = DevelopmentConfig().DATABASE_OBJ


@covid_new_cases_bp.route('/covid_new_cases/json/<location>', methods=['GET'])
def get_covid_new_cases_per_location(location: str):
    location = location.capitalize()
    result = find_covid_new_cases(database, location)
    record_count = result.count()
    return {
        'result': list(result),
        'result_count': record_count,
        'route': f'/covid_new_cases/json/{location}',
        'status': 200,
    }


@covid_new_cases_bp.route('/covid_new_cases/table/<location>', methods=['GET'])
def get_covid_new_cases_per_location_html(location: str):
    location = location.capitalize()
    result = find_covid_new_cases(database, location)
    return render_template(
        'covid_new_cases.html',
        output=list(result),
        location=location
    )


@covid_new_cases_bp.route('/covid_new_cases/chart/<location>', methods=['GET'])
def get_covid_new_cases_chart(location: str):
    location = location.capitalize()
    return render_template(
        'covid_new_cases_chart.html',
        location=location
    )
