from application import app


@app.route('/', methods=['GET'])
def home():
    return {
        'result': {
            'api': 'covid-api',
            'documentation': '<insert_url>',
            'endpoints': {
                'json_format': [
                    '/covid_summary/json/<location>',
                    '/covid_new_cases/json/<location>',
                ],
                'tables': [
                    '/covid_summary/table/<location>',
                    '/covid_new_cases/table/<location>',
                ],
                'chart': [
                    '/covid_new_cases/chart/<location>'
                ]
            }
        },
        'route': '/',
        'status': 200,
    }
