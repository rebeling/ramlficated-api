# -*- coding: utf-8 -*-
import ramlfications
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging

from utils.resource import resource_restructure
from tornadoview import RamlowView

TORNADO_URI_PARAM_PATTERN = [('{', '(?P<'), ('}', '>[^\/]+)')]
TORNADO_PORT = 8888


def make_app():

    # 1. collect all methods for same endpoint pattern
    api = ramlfications.parse('etc/ramls/documents-api.raml')
    _resources = resource_restructure(api,
                                      replacer=TORNADO_URI_PARAM_PATTERN)

    endpoints = []
    for rule, resources in _resources.items():
        # print 'endpoint create', rule, resources
        endpoints.append((rule,
                          RamlowView,
                          dict(resources=resources, api=api)))

    application = tornado.web.Application(endpoints, debug=True)
    return application


if __name__ == "__main__":
    app = make_app()
    app.listen(TORNADO_PORT)
    enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
