# -*- coding: utf-8 -*-
# import tornado.ioloop
import tornado.web

# import tornado.ioloop
# import tornado.web
# from datetime import datetime
# import urlparse
# from bson.json_util import dumps
import json
from utils import post_validator
from utils import response_info


class RamlowView(tornado.web.RequestHandler):

    def initialize(self, resources, api):

        # self.db_api = DatabaseAPI()

        self.resources = resources
        self.base_url = api.base_uri
        print "initialize resources", resources, api

    def write_error(self, status_code, **kwargs):
        print 'In get_error_html. status_code: ', status_code
        # if status_code in [403, 404, 500, 503]:
        self.write('Error %s' % status_code)

    def prepare(self):
        print 'In prepare...', self.request

    def _response(self, success, doc, responses, code=None):

        doc, code = response_info(success,
                                  doc,
                                  responses,
                                  code=code,
                                  request_url=self.request.full_url)
                                  # request_url=self.request.uri)

        self.set_header('Link', self.base_url)
        self.set_header('Content-Type', 'application/json')
        self.set_status(400)
        self.write(json.dumps(doc))

    def post(self):
        resource = self.resources['POST']
        print "post request resource", resource

        data = json.loads(self.request.body)
        docs = post_validator(data, resource.body[0].schema)

        success = True # self.db_api.add(docs)
        self._response(success, data, resource.responses)

    def get(self, id):
        resource = self.resources['GET']
        print "get request resource", resource

        success, doc = True, {} # self.db_api.get(id)
        self._response(success, data, resource.responses)

    def put(self, id):
        print id
        resource = self.resources['PUT']
        print "put request resource", resource

        success = False # True # self.db_api.update(id, json.loads(self.request.body))
        self._response(success, None, resource.responses)

    def delete(self, id):
        resource = self.resources['DELETE']
        print "delete request resource", resource

        success = True # self.db_api.delete(id)
        self._response(success, None, resource.responses)
