# -*- coding: utf-8 -*-
"""Interface to a database instance.

Provide a class to communicate from endpoint to storage instance.
Let it be elasticsearch or postgres - interaction with api will be
the same more or less.

Lets try: pyelasticsearch
http://pyelasticsearch.readthedocs.org/en/latest/api/?highlight=search#pyelasticsearch.ElasticSearch.search
"""
from pyelasticsearch import ElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError


class DatabaseAPI(object):
    """Storage interface between API and store instance."""
    def __init__(self):
        super(DatabaseAPI, self).__init__()
        self.es = ElasticSearch()
        self.index = 'myindex'
        self.doc_type = 'book'

    def _resolve(self, index, doc_type):
        index = index if index else self.index
        doc_type = doc_type if doc_type else self.doc_type
        return index, doc_type

    def add(self, doc, index=None, doc_type=None):
        """POST case: add new document."""
        index, doc_type = self._resolve(index, doc_type)
        res = self.es.index(index, doc_type, doc, id=doc.get("id"))
        success = True if res['created'] else False
        return success

    def get_documents(self, query=None):
        """GET case: documents by query."""
        # multi_get ids ?!
        # search(query[, other kwargs listed below])
        return []

    def get(self, id, index=None, doc_type=None):
        """GET case: document by id."""
        index, doc_type = self._resolve(index, doc_type)

        try:
            res = self.es.get(index, doc_type, id)
            doc = res.get('_source')
            success = True if doc else False
        except ElasticHttpNotFoundError:
            success, doc = False, None

        return success, doc

    def update(self, id, data, index=None, doc_type=None):
        """PUT / PATCH case: update whole or partial document."""
        index, doc_type = self._resolve(index, doc_type)

        try:
            print "data", data
            res = self.es.update(index, doc_type, id, **data)
            print res
            success = True
        except ElasticHttpNotFoundError:
            success = False

        return success

    def delete(self, id, index=None, doc_type=None):
        """DELETE case: delete document by id."""
        index, doc_type = self._resolve(index, doc_type)

        try:
            res = self.es.delete(index, doc_type, id)
            success = True
        except ElasticHttpNotFoundError:
            success = False

        return success
