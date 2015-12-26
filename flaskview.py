# -*- coding: utf-8 -*-
from flask import request
from flask.views import View
from jsonschema import validate
import json
from databaseapi import DatabaseAPI
from flask import jsonify


def example(responses, code=None, key='description'):
    # print resource_responses
    example = None
    print responses
    for res in responses:
        print res
        if code:
            if code == res.code:
                print ">>", res.raw
                example = res.raw[code][key]
    print example
    return example


class RamlowView(View):

    def __init__(self, resources, api):
        self.methods = resources.keys()
        self.resources = resources
        self.db_api = DatabaseAPI()
        self.base_url = api.base_uri

    def _message(self, responses, code, doc):
        doc = example(responses, code=code)
        return {'status': code, 'message': '{} {}'.format(doc, request.url)}

    def _response(self, success, doc, responses, code=None):

        if code == 500:
            doc = {'status': 500,
                   'message': '{} {}'.format(doc, request.url)}
        else:
            first = '2' if success else '4'
            x = [x for x in responses if repr(x.code).startswith(first)][0]
            code = x.code
            if doc is None or first == '4':
                doc = self._message(responses, code, doc)

        # create response object
        resp = jsonify(doc)
        resp.status_code = code
        resp.headers['Link'] = self.base_url
        return resp

    def _get_id(self, resource, kwargs):
        return kwargs[getattr(resource, 'uri_params')[0].name]

    def dispatch_request(self, **kwargs):

        try:
            request_method = request.method
            resource = self.resources[request_method]
            responses = resource.responses

            if request_method == 'POST':
                # Retrieve a document, validate and send to db.

                doc = json.loads(request.data)
                validate(doc, resource.body[0].schema)
                success = self.db_api.add(doc)
                return self._response(success, doc, responses)

            else:
                id = self._get_id(resource, kwargs)

                if request_method == 'GET':
                    success, doc = self.db_api.get(id)
                    return self._response(success, doc, responses)

                elif request_method == 'PUT':
                    data = json.loads(request.data)
                    success = self.db_api.update(id, data)
                    return self._response(success, None, responses)

                elif request_method == 'DELETE':
                    success = self.db_api.delete(id)
                    return self._response(success, None, responses)

            raise NotImplementedError

        except Exception, e:
            return self._response(False, e, responses, code=500)
