# -*- coding: utf-8 -*-
from flask import Flask
from flaskview import RamlowView as raml_view
import ramlfications


app = Flask(__name__)

import logging
file_handler = logging.FileHandler('logs/app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


def flaskify_ramlfication(api):
    flask_resources = {}
    for resource in api.resources:
        # fix url param pattern syntax for {} to <>
        resource_path = resource.path.replace('{', '<').replace('}', '>')
        flask_resources_pr = flask_resources.get(resource_path, {})
        flask_resources_pr.update({resource.method.upper(): resource})
        flask_resources[resource_path] = flask_resources_pr
    return flask_resources


if __name__ == "__main__":

    raml_file = 'ramls/articles-api.raml'
    api = ramlfications.parse(raml_file)
    print api.title

    # 1. collect all methods for same endpoint pattern
    flask_resources = flaskify_ramlfication(api)

    print "flask_resources", flask_resources
    # print "api.schemas", api.schemas[0]

    # 2. add url to app
    for rule, resources in flask_resources.items():
        app.add_url_rule(rule,
                         view_func=raml_view.as_view(rule,
                                                     resources=resources,
                                                     api=api),
                         methods=resources.keys())

    app.run(debug=True)
    app.logger.info('app started')
