# -*- coding: utf-8 -*-

import logging
file_handler = logging.FileHandler('logs/app.log')
from tornadoview import RamlowView
import tornado.ioloop
import tornado.web
import ramlfications


def flaskify_ramlfication(api):
    flask_resources = {}
    for resource in api.resources:
        # fix url param pattern syntax for {} to <>
        resource_path = resource.path.replace('{', '(?P<').replace('}', '>[^\/]+)')
        flask_resources_pr = flask_resources.get(resource_path, {})
        flask_resources_pr.update({resource.method.upper(): resource})
        flask_resources[resource_path] = flask_resources_pr
    return flask_resources


# if __name__ == "__main__":

#     raml_file = 'ramls/articles-api.raml'
#     api = ramlfications.parse(raml_file)
#     print api.title

#     # 1. collect all methods for same endpoint pattern
#     flask_resources = flaskify_ramlfication(api)

#     print "flask_resources", flask_resources
#     # print "api.schemas", api.schemas[0]

#     # 2. add url to app
#     for rule, resources in flask_resources.items():
#         app.add_url_rule(rule,
#                          view_func=raml_view.as_view(rule,
#                                                      resources=resources,
#                                                      api=api),
#                          methods=resources.keys())

#     app.run(debug=True)
#     app.logger.info('app started')


def make_app():

    # 1. collect all methods for same endpoint pattern
    raml_file = 'ramls/articles-api.raml'
    api = ramlfications.parse(raml_file)
    flask_resources = flaskify_ramlfication(api)

    endpoints = []
    for rule, resources in flask_resources.items():
        print 'endpoint create', rule, resources
        endpoints.append((rule,
                          RamlowView,
                          dict(resources=resources, api=api)))

    # endpoints = [
    #     (r"/", RamlowView),
    #     # (r"/blog/([0-9]+)", Blog, dict(connection = Connection()) ),
    #     # (r"/blog/", Blog, dict(connection =  Connection()) ),
    #     # (r"/blogs/", Blogs, dict(connection =  Connection()) ),
    # ]

    application = tornado.web.Application(endpoints, debug=True)
    return application


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
