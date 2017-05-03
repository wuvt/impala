#!/usr/bin/env python3

from impala.api.v1 import bp


@bp.route('/')
def index():
    return 'Hello world!'
