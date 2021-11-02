from flask import Flask
from application.config.Config import DevelopmentConfig, Config
from application.controllers.home_controller import home_bp
from application.controllers.covid_summary_controller import covid_summary_bp
from application.controllers.covid_new_cases_controller import covid_new_cases_bp
from application.controllers.covid_new_deaths_controller import covid_new_deaths_bp
from application.controllers.vaccination_summary import vaccination_bp


def init_app(config: Config):
    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,
    )
    app.config.from_object(config)
    with app.app_context():
        app.register_blueprint(home_bp)
        app.register_blueprint(covid_summary_bp)
        app.register_blueprint(covid_new_cases_bp)
        app.register_blueprint(covid_new_deaths_bp)
        app.register_blueprint(vaccination_bp)
        return app
