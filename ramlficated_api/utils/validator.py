# -*- coding: utf-8 -*-
from jsonschema import validate


def post_validator(data, schema):
    docs = data if isinstance(data, list) else [data]
    for obj in docs:
        validate(obj, schema)
    return docs

