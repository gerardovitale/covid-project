from flask import Flask
from Config import DevelopmentConfig


database = DevelopmentConfig().DATABASE_OBJ

app = Flask(
    __name__, 
    template_folder=DevelopmentConfig.TEMPLATE_FOLDER, 
    static_folder=DevelopmentConfig.STATIC_FOLDER,
)

import application.controllers.controllers
