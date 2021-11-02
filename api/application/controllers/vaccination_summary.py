from application import DevelopmentConfig
from application.controllers import vaccination_bp

database = DevelopmentConfig().DATABASE_OBJ


@vaccination_bp.route('/vaccination_summary/json/<location>', methods=['GET'])
def get_vaccination_summary_json(location: str) -> dict:
    pass
