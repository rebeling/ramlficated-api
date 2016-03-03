# -*- coding: utf-8 -*-
from flask import Flask
import logging
import ramlfications
import sys

from flaskview import RamlowView as raml_view
from utils.resource import resource_restructure
from utils.configuration import config
from databaseapi import DatabaseAPI

FLASK_URI_PARAM_PATTERN = [('{', '<'), ('}', '>')]


def create_app(name, config, db_api):
    """Create a flask app with endpoints of raml config."""
    app = Flask(name)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)

    api = ramlfications.parse('etc/ramls/documents_api.raml')

    # 1. collect all methods for same endpoint pattern
    _resources = resource_restructure(api, replacer=FLASK_URI_PARAM_PATTERN)

    # 2. add url to app
    for rule, resources in _resources.items():
        app.add_url_rule(rule,
                         view_func=raml_view.as_view(rule,
                                                     resources=resources,
                                                     api=api,
                                                     db_api=db_api),
                         methods=resources.keys())
    return app


if __name__ == "__main__":
    db_api = DatabaseAPI(config)
    app = create_app(__name__, config, db_api)
    app.run(debug=True)
    app.logger.info('app started')
