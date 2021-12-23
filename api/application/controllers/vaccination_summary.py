from application import DevelopmentConfig
from application.controllers import vaccination_bp
from application.services.vaccination_summary_service import find_vaccination_summary, calculate_vaccination_rate

database = DevelopmentConfig().DATABASE_OBJ


@vaccination_bp.route('/vaccination_summary/json/<location>', methods=['GET'])
def get_vaccination_summary_json(location: str) -> dict:
    days = 16
    location = location.capitalize()
    mongo_data = find_vaccination_summary(database, days, location)
    mongo_data = list(mongo_data)
    record_count = mongo_data.__len__()
    summary = calculate_vaccination_rate(mongo_data)
    return {
        'result': list(summary),
        'result_count': record_count,
        'route': f'/covid_summary/json/{location}',
        'status': 200,
    }
