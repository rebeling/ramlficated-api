# -*- coding: utf-8 -*-
from flask import request
from flask.views import View
import json
from databaseapi import DatabaseAPI
from flask import jsonify
from utils import post_validator
from utils import response_info


class RamlowView(View):

    def __init__(self, resources, api):
        self.methods = resources.keys()
        self.resources = resources
        self.db_api = DatabaseAPI()
        self.base_url = api.base_uri

    def _response(self, success, doc, responses, code=None):

        doc, code = response_info(success, doc, responses, code=code, request_url=request.url)

        # create response object
        resp = jsonify(results=doc) if isinstance(doc, list) else jsonify(doc)
        resp.status_code = code
        resp.headers['Link'] = self.base_url
        return resp

    def _get_id(self, resource, kwargs):
        return kwargs[getattr(resource, 'uri_params')[0].name]

    def dispatch_request(self, **kwargs):

        try:
            request_method = request.method
            resource = self.resources[request_method]

            if request_method == 'POST':
                # Retrieve a document or documents, validate and send to db.

                data = json.loads(request.data)
                docs = post_validator(data, resource.body[0].schema)

                success = self.db_api.add(docs)
                return self._response(success, data, resource.responses)

            else:
                id = self._get_id(resource, kwargs)

                if request_method == 'GET':
                    success, doc = self.db_api.get(id)
                    return self._response(success, doc, resource.responses)

                elif request_method == 'PUT':
                    success = self.db_api.update(id, json.loads(request.data))
                    return self._response(success, None, resource.responses)

                elif request_method == 'DELETE':
                    success = self.db_api.delete(id)
                    return self._response(success, None, resource.responses)

            raise NotImplementedError

        except Exception, e:
            return self._response(False, e, resource.responses, code=500)
