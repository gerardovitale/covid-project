from application import init_app, DevelopmentConfig


if __name__ == "__main__":
    app = init_app(config=DevelopmentConfig())
    app.run(
        host=DevelopmentConfig.HOST,
        port=DevelopmentConfig.PORT
    )
