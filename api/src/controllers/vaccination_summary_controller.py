from flask import request, render_template, Blueprint

from src import DevelopmentConfig
from src.controllers.helpers import get_params_pagination
from src.services.covid_summary_service import paginate_mongo_data
from src.services.vaccination_summary_service import find_vaccination_summary, calculate_vaccination_rate

database = DevelopmentConfig().DATABASE_OBJ
vaccination_bp = Blueprint('vaccination_bp', __name__)


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


@vaccination_bp.route('/vaccination_summary/table/<location>', methods=['GET'])
def get_vaccination_summary_table(location: str) -> str:
    days = 16
    location = location.capitalize()
    start, width, nav_offsets = get_params_pagination(request)
    mongo_data = find_vaccination_summary(database, days, location)
    mongo_data = paginate_mongo_data(mongo_data, start, width)
    mongo_data = list(mongo_data)
    record_count = mongo_data.__len__()
    summary = calculate_vaccination_rate(mongo_data)
    return render_template(
        'vaccination_summary.html',
        output=summary,
        location=location,
        days=days,
        record_count=record_count,
        nav_path=request.path,
        nav_offsets=nav_offsets
    )
