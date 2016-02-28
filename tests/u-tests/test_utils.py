# -*- coding: utf-8 -*-
from codecs import open
import json
import ramlfications

from ramlficated_api.utils.responses import message
from ramlficated_api.utils.validator import post_validator
from ramlficated_api.utils.resource import resource_restructure


def test_message():
    x = message({}, 500, None, "http://api")
    assert x == {'message': 'None http://api', 'status': 500}


def test_post_validator():
    with open('etc/ramls/data/document-schema.json', 'r', 'utf-8') as fs:
        schema = json.loads(fs.read())
    with open('etc/ramls/data/document-example.json', 'r', 'utf-8') as fd:
        doc = json.loads(fd.read())
    assert post_validator(doc, schema) == [doc]


def test_resource_restructure_flask_url_pattern():
    from ramlficated_api.main_flask import FLASK_URI_PARAM_PATTERN
    api = ramlfications.parse('etc/ramls/documents-api.raml')
    _resources = resource_restructure(api,
                                      replacer=FLASK_URI_PARAM_PATTERN)
    assert '/documents/<id>' in _resources.keys()


def test_resource_restructure_tornado_url_pattern():
    from ramlficated_api.main_tornado import TORNADO_URI_PARAM_PATTERN
    api = ramlfications.parse('etc/ramls/documents-api.raml')
    _resources = resource_restructure(api,
                                      replacer=TORNADO_URI_PARAM_PATTERN)
    assert '/documents/(?P<id>[^\\/]+)' in _resources.keys()
