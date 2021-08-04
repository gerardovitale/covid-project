from flask import Request


def get_url_query_params(req: Request):
    location = req.args.get('location').capitalize()
    days = int(req.args.get('days')) \
            if req.args.get('days') is not None \
            else 10
    return location, days