# -*- coding: utf-8 -*-
import json
from flask import jsonify, request, views
from utils.responses import response_info
from utils.validator import post_validator


class RamlowView(views.View):

    def __init__(self, resources, api, db_api):
        self.methods = resources.keys()
        self.resources = resources
        self.db_api = db_api
        self.base_url = api.base_uri

    def _response(self, success, doc, responses, code=None):
        """Create response object."""
        doc, code = response_info(success, doc, responses,
                                  code=code, request_url=request.url)
        resp = jsonify(results=doc) if isinstance(doc, list) else jsonify(doc)
        resp.status_code = code
        resp.headers['Link'] = self.base_url
        return resp

    def _get_doc_id(self, resource, kwargs):
        """Get key for the id from uriParameters / uri_params."""
        return kwargs[getattr(resource, 'uri_params')[0].name]

    def dispatch_request(self, **kwargs):
        """Overwrite dispatcher for intended behavior at request time."""
        # print "dispatch_request", request.method

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
                id = self._get_doc_id(resource, kwargs)

                if request_method == 'GET':
                    success, doc = self.db_api.recieve(id)
                    return self._response(success, doc, resource.responses)

                elif request_method == 'PUT':
                    success = self.db_api.update(id, json.loads(request.data))
                    return self._response(success, None, resource.responses)

                elif request_method == 'DELETE':
                    success = self.db_api.delete(id)
                    return self._response(success, None, resource.responses)

        except Exception, e:
            return self._response(False, e, resource.responses, code=500)
