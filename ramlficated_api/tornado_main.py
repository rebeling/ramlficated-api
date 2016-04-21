# -*- coding: utf-8 -*-
import tornado.log
import tornado.ioloop
import tornado.web
import ramlfications

from utils.resource import resource_restructure
from utils.configuration import config
from tornado_view import RamlowView as ramlow_view

TORNADO_URI_PARAM_PATTERN = [('{', '(?P<'), ('}', '>[^\/]+)')]
TORNADO_PORT = 8888


def make_app():

    # 1. collect all methods for same endpoint pattern
    api = ramlfications.parse('etc/ramls/documents-api.raml')
    _resources = resource_restructure(api, replacer=TORNADO_URI_PARAM_PATTERN)

    # 2. add url to app
    endpoints = []
    for rule, resources in _resources.items():
        # url, profilehandler, kwargs used in profilehandler
        uri_kwargs = dict(resources=resources, api=api, config=config)
        endpoints.append((rule, ramlow_view, uri_kwargs))

    return tornado.web.Application(endpoints, debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(TORNADO_PORT)
    tornado.log.enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
