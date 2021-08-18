from controllers.controllers import app, DevelopmentConfig


if __name__ == "__main__":
    app.config.from_object(DevelopmentConfig())
    app.run(
        host=DevelopmentConfig.HOST,
        port=DevelopmentConfig.PORT
    )