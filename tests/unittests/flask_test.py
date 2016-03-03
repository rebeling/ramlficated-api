# -*- coding: utf-8 -*-
from codecs import open
import json
import mock
import ramlfications
import unittest

from ramlficated_api.databaseapi import DatabaseAPI
from ramlficated_api.main_flask import create_app
from ramlficated_api.utils.configuration import config


# mock the elasticsearch interface functions: get, ..
with open('etc/ramls/data/document_example.json', 'r', 'utf-8') as f:
    mock_doc = json.loads(f.read())

db_api_mock = DatabaseAPI(config)
db_api_mock.recieve = mock.MagicMock(return_value=(True, mock_doc))
db_api_mock.add = mock.MagicMock(return_value=True)
db_api_mock.update = mock.MagicMock(return_value=True)
db_api_mock.delete = mock.MagicMock(return_value=True)

# create app and load raml config as api
app = create_app('test', config, db_api_mock)
api = ramlfications.parse('etc/ramls/documents_api.raml')


class TestRoutes(unittest.TestCase):

    # this method is run before each test
    def setUp(self):
        self.client = app.test_client()  # we instantiate a flask test client

    def test_get_document_by_id(self):
        response = self.client.get('/documents/%s' % 'anId')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.headers['Link'], api.base_uri)
        self.assertEqual(json.loads(response.data), mock_doc)

    def test_post_document(self):
        response = self.client.post('/documents',
                                    data=json.dumps(mock_doc),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data), mock_doc)

    def test_put_document(self):
        key = mock_doc.keys()[0]
        partial_doc = {key: mock_doc[key]}
        response = self.client.put('/documents/anId',
                                    data=json.dumps(partial_doc),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status, '204 NO CONTENT')
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_delete_document(self):
        response = self.client.delete('/documents/anId')
        self.assertEqual(response.status, '204 NO CONTENT')

    def test_not_implemented(self):
        response = self.client.patch('/documents',
                                    data=json.dumps(mock_doc),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

    def test_exception(self):
        response = self.client.post('/documents',
                                    data=None,
                                    headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status, '500 INTERNAL SERVER ERROR')


if __name__ == '__main__':
    unittest.main()
