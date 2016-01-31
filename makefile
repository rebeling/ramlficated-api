.PHONY: docs clean all prod virtualenv install install-requirements

VIRTUALENV_DIR=${PWD}/env
PIP=${VIRTUALENV_DIR}/bin/pip
PYTHON=${VIRTUALENV_DIR}/bin/python
APP_PATH=${PWD}

# the `all` target will install everything necessary to develop and deploy
all: prod

# the `prod` target will create the runnable distribution without tests
prod: virtualenv install

virtualenv:
	if [ ! -e ${VIRTUALENV_DIR}/bin/pip ]; then virtualenv ${VIRTUALENV_DIR} --no-site-packages; fi

install: install-requirements
	${PYTHON} setup.py develop

install-requirements: virtualenv
	${PIP} install -r requirements.txt


docs:
	raml2html ramls/documents-api.raml -o docs/documents-api.html
	raml2md ramls/documents-api.raml -o docs/documents-api.md
	open docs/documents-api.html && open docs/documents-api.md

run-flask:
	env/bin/python ramlficated-api/main-flask.py

flask-calls:
	http post :5000/documents < data/document-example.json
	http post :5000/documents < data/document-examples.json
	http post :5000/documents id="42" note="500 on validation, missing fields"
	http :5000/documents/1 -v
	http put :5000/documents/1 script="ctx._source.views+=1"
	http put :5000/documents/1 doc:='{"title": "Demons"}'
	http :5000/documents/1 -v
	http delete :5000/documents/1 -v
	http delete :5000/documents/2 -v
	http delete :5000/documents/3 -v
	http delete :5000/documents/4 -v

run-tornado:
	env/bin/python ramlficated-api/main-tornado.py

tornado-calls:
	http post :8888/documents < data/document-example.json
	http post :8888/documents < data/document-examples.json
	http post :8888/documents id="42" note="500 on validation, missing fields"
	http :8888/documents/1 -v
	http put :8888/documents/1 script="ctx._source.views+=1"
	http put :8888/documents/1 doc:='{"title": "Demons"}'
	http :8888/documents/1 -v
	http delete :8888/documents/1 -v
	http delete :8888/documents/2 -v
	http delete :8888/documents/3 -v
	http delete :8888/documents/4 -v

tree:
	ramlfications tree documents.raml -v

clean:
	rm -fv .DS_Store .coverage
	rm -rfv .cache
	find ${APP_PATH} -name '*.pyc' -exec rm -fv {} \;
	find ${APP_PATH} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf *.egg-info logs/*.log docs/*.html docs/*.md
	rm -Rf env
