from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
    return {
        'result': {
            'api': 'covid-api',
            'documentation': '<isert_url>',
            'endpoints': [
                '/',
            ],
        },
        'route': '/',
        'status': 200,
    }
    