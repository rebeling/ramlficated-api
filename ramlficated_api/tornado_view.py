# -*- coding: utf-8 -*-
import tornado.web
import json

from database_api import DatabaseAPI
from utils.responses import response_info
from utils.validator import post_validator


class RamlowView(tornado.web.RequestHandler):

    def initialize(self, resources, api, config):
        self.db_api = DatabaseAPI(config)
        self.resources = resources
        self.base_url = api.base_uri
        print "initialize resources ...api?", resources, api

    def _response(self, success, doc, responses, code=None):
        """Preapare response and write back."""
        doc, code = response_info(success,
                                  doc,
                                  responses,
                                  code=code,
                                  request_url=self.request.full_url)

        self.set_header('Link', self.base_url)
        self.set_header('Content-Type', 'application/json')
        self.set_status(code)
        self.write(json.dumps(doc))

    def post(self):
        resource = self.resources['POST']
        data = json.loads(self.request.body)
        docs = post_validator(data, resource.body[0].schema)
        success = self.db_api.add(docs)
        self._response(success, data, resource.responses)

    def get(self, id):
        resource = self.resources['GET']
        success, doc = self.db_api.get(id)
        self._response(success, doc, resource.responses)

    def put(self, id):
        resource = self.resources['PUT']
        success = self.db_api.update(id, json.loads(self.request.body))
        self._response(success, None, resource.responses)

    def delete(self, id):
        resource = self.resources['DELETE']
        success = self.db_api.delete(id)
        self._response(success, None, resource.responses)

    def write_error(self, status_code, **kwargs):
        """Catch and handle tornado error."""
        print 'In get_error_html. status_code: ', status_code
        try:
            # handle exception here
            # get request and look up self.resources
            # if status_code in [403, 404, 500, 503]:
            error_class, message, traceback_object = kwargs["exc_info"]
        except Exception, e:
            message = "Woha, %s" % e

        self.write('%s Error, message: %s' % (status_code, message))

    def prepare(self):
        """Dispatch request before processed."""
        print 'In prepare...', self.request
