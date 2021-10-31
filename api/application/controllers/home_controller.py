from flask import Blueprint

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/', methods=['GET'])
def home():
    return {
        'result': {
            'api': 'covid-api',
            'documentation': '<insert_url>',
            'endpoints': {
                'json_format': [
                    '/covid_summary/json/<location>',
                    '/covid_new_cases/json/<location>',
                    '/covid_new_deaths/json/<location>',
                ],
                'tables': [
                    '/covid_summary/table/<location>',
                    '/covid_new_cases/table/<location>',
                    '/covid_new_deaths/table/<location>',
                ],
                'chart': [
                    '/covid_new_cases/chart/<location>',
                    '/covid_new_deaths/chart/<location>',
                ]
            }
        },
        'route': '/',
        'status': 200,
    }
