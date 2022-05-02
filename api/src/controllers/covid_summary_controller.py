from flask import Blueprint, render_template, request

from config.Config import DevelopmentConfig
from controllers.helpers import get_params_covid_summary, get_params_pagination
from services.covid_summary_service import find_covid_summary, paginate_mongo_data, enhance_data

covid_summary_bp = Blueprint('covid_summary_bp', __name__)
database = DevelopmentConfig().DATABASE_OBJ


@covid_summary_bp.route('/covid_summary/json/<location>', methods=['GET'])
def get_covid_summary(location: str):
    location, days = get_params_covid_summary(request, location)
    summary = find_covid_summary(database, days, location)
    result = enhance_data(summary)
    return {
        'result': result,
        'result_count': result.__len__(),
        'route': f'/covid_summary/json/{location}',
        'status': 200,
    }


@covid_summary_bp.route('/covid_summary/table/<location>', methods=['GET'])
def get_covid_summary_html(location: str):
    location, days = get_params_covid_summary(request, location)
    start, width, nav_offsets = get_params_pagination(request)
    summary = find_covid_summary(database, days, location)
    summary = paginate_mongo_data(summary, start, width)
    summary = enhance_data(summary)
    record_count = summary.__len__()
    return render_template(
        'covid_summary.html',
        output=summary,
        location=location,
        days=days,
        record_count=record_count,
        nav_path=request.path,
        nav_offsets=nav_offsets
    )


@covid_summary_bp.route('/covid_summary/chart/<location>', methods=['GET'])
def get_covid_dashboard(location: str):
    location, days = get_params_covid_summary(request, location)
    return render_template(
        'covid_summary_dashboard.html',
        location=location,
        days=days,
    )
