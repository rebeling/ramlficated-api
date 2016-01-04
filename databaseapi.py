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
        self.index = 'raml_api_index'
        self.doc_type = 'document'

    def _resolve(self, index, doc_type):
        index = index if index else self.index
        doc_type = doc_type if doc_type else self.doc_type
        return index, doc_type

    def add(self, docs, index=None, doc_type=None, overwrite_existing=False):
        """POST case: add new document or bulk of documents."""
        index, doc_type = self._resolve(index, doc_type)

        bulk = []
        for doc in docs:
            bulk.append(self.es.index_op(doc,
                                         doc_type=doc_type,
                                         overwrite_existing=overwrite_existing,
                                         **{"id": doc.get("id")}))
        res = self.es.bulk(bulk,
                           doc_type=doc_type,
                           index=index)

        print res

        success = True if res['errors'] is False else False
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
            res = self.es.update(index, doc_type, id, **data)
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
