# -*- coding: utf-8 -*-
from flask import Flask
import logging
import ramlfications

from flaskview import RamlowView as raml_view
from utils.resource import resource_restructure

app = Flask(__name__)
app.logger.addHandler(logging.FileHandler('logs/app.log'))
app.logger.setLevel(logging.INFO)

FLASK_URI_PARAM_PATTERN = [('{', '<'), ('}', '>')]


if __name__ == "__main__":

    api = ramlfications.parse('etc/ramls/documents-api.raml')

    # 1. collect all methods for same endpoint pattern
    _resources = resource_restructure(api,
                                      replacer=FLASK_URI_PARAM_PATTERN)

    # 2. add url to app
    for rule, resources in _resources.items():
        app.add_url_rule(rule,
                         view_func=raml_view.as_view(rule,
                                                     resources=resources,
                                                     api=api),
                         methods=resources.keys())

    app.run(debug=True)
    app.logger.info('app started')
