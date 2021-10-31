from flask import Blueprint, render_template, request

from application import DevelopmentConfig
from application.controllers.helpers import (get_params_covid_summary,
                                             get_params_pagination)
from application.services.covid_summary_service import (calculate_rates,
                                                        find_covid_summary,
                                                        paginate_mongo_data)

covid_summary_bp = Blueprint('covid_summary_bp', __name__)
database = DevelopmentConfig().DATABASE_OBJ


@covid_summary_bp.route('/covid_summary/json/<location>', methods=['GET'])
def get_covid_summary(location: str):
    location, days = get_params_covid_summary(request, location)
    summary = find_covid_summary(database, days, location)
    record_count = summary.count()
    return {
        'result': list(summary),
        'result_count': record_count,
        'route': f'/covid_summary/json/{location}',
        'status': 200,
    }


@covid_summary_bp.route('/covid_summary/table/<location>', methods=['GET'])
def get_covid_summary_html(location: str):
    location, days = get_params_covid_summary(request, location)
    start, width, nav_offsets = get_params_pagination(request)
    summary = find_covid_summary(database, days, location)
    summary = paginate_mongo_data(summary, start, width)
    record_count = summary.count()
    summary = calculate_rates(summary)
    return render_template(
        'covid_summary.html',
        output=summary,
        location=location,
        days=days,
        record_count=record_count,
        nav_path=request.path,
        nav_offsets=nav_offsets
    )
