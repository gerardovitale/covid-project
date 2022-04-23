from config.Config import DevelopmentConfig
from entrypoint import init_app


if __name__ == "__main__":
    app = init_app(config=DevelopmentConfig())
    app.run(
        host=DevelopmentConfig.HOST,
        port=DevelopmentConfig.PORT
    )
