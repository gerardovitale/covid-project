from typing import Any, Dict, Tuple
from flask import Request


def get_params_covid_summary(req: Request) -> Tuple[str, int]:
    location = req.args.get('location').capitalize()
    days = req.args.get('days') or 10
    return location, int(days)


def get_navigation_offsets(offset1, offset2, increment) -> Dict[str, Any]:
    offsets = {}
    offsets['Next'] = {'top_offset': offset2 + increment,
                       'bottom_offset': offset1 + increment}
    offsets['Previous'] = {'top_offset': max(offset2 - increment, 0), 
                           'bottom_offset': max(offset1 - increment, 0)}
    return offsets


def get_params_pagination(req: Request) -> Tuple[int, int, Dict[str, Any]]:
    start = req.args.get('start') or 0
    start = int(start)
    end = req.args.get('end') or 20
    end = int(end)
    width = end - start
    nav_offsets = get_navigation_offsets(start, end, 20)
    return start, width, nav_offsets
