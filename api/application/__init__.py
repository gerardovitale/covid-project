from flask import Flask
from application.config.Config import DevelopmentConfig


database = DevelopmentConfig().DATABASE_OBJ

app = Flask(
    __name__, 
    template_folder=DevelopmentConfig.TEMPLATE_FOLDER, 
    static_folder=DevelopmentConfig.STATIC_FOLDER,
)

import application.controllers.home_controller
import application.controllers.covid_summary_controller
import application.controllers.covid_new_cases_controller
import application.controllers.covid_new_deaths_controller
