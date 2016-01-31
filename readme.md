Ramlficated CRUD-api
--------------------

Define an api in raml and provide server with flask or tornado to deal
with the requests. The requests do crud with documents against an elasticsearch index.

Blog post about it: http://blog.rebeling.net/blog/ramlficated-api/


Usage
------
Make project, start server, turn on elasticsearch and run the examples. The make
calls use httpie https://pypi.python.org/pypi/httpie that is not build with this
package.

    make
    make run-flask
    ~/Documents/elasticsearch-2.1.1/bin/elasticsearch
    brew install httpie
    make flask-calls



Todos:
-----

1. documentation: api doc to md
2. research synergies: jsonschema validation - es mapping - documents
