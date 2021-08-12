from flask import Request


def get_query_url_params_covid_summary(req: Request):
    location = req.args.get('location').capitalize()
    days = req.args.get('days') or 10
    return location, int(days)
