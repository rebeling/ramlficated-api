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

    def __init__(self, config):
        self.es = ElasticSearch()
        self.index = config['index']
        self.doc_type = config['doc_type']

    def _resolve(self, index, doc_type):
        return (index if index else self.index,
                doc_type if doc_type else self.doc_type)

    def _index_op(self, doc, doc_type, overwrite_existing):
        return self.es.index_op(doc, doc_type=doc_type,
                                overwrite_existing=overwrite_existing,
                                **dict(id=doc.get("id")))

    def add(self, docs, index=None, doc_type=None, overwrite_existing=False):
        """POST case: add new document or bulk of documents."""
        index, doc_type = self._resolve(index, doc_type)
        bulk = [self._index_op(d, doc_type, overwrite_existing) for d in docs]
        res = self.es.bulk(bulk, doc_type=doc_type, index=index)
        success = True if res['errors'] is False else False
        return success

    def get_documents(self, query=None, index=None, doc_type=None):
        """GET case: documents by query."""
        index, doc_type = self._resolve(index, doc_type)
        # multi_get ids ?!
        # search(query[, other kwargs listed below])
        return []

    def recieve(self, id, index=None, doc_type=None):
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
