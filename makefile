.PHONY: setup virtualenv install ci unittest docs clean

VIRTUALENV_DIR = ${PWD}/env
PIP = ${VIRTUALENV_DIR}/bin/pip
RAML = etc/ramls
APP = ramlficated_api

help:
	@echo '    setup ........ sets up project'
	@echo '    docs ......... creates docs from etc/ramls file'
	@echo '    unittest ..... runs unittest'
	@echo '    ci ........... sets up project and run all tests'
	@echo '    clean ........ cleans project'
	@echo '    release ...... releases project to pypi'


# the `setup` target will create the runnable distribution without tests
setup: virtualenv install

virtualenv:
	if [ ! -e ${PIP} ]; then virtualenv ${VIRTUALENV_DIR} --no-site-packages; fi

install: virtualenv
	${PIP} install -r requirements.txt
	${VIRTUALENV_DIR}/bin/python setup.py develop

# set up testing targets and a ci target for continuous integration
ci: unittest


# Testing

COVERAGE_RUN=${VIRTUALENV_DIR}/bin/coverage run

unittest: unittest_flask unittest_tornado
	${COVERAGE_RUN} --source ${APP}/utils -m py.test -s tests/unit_utils/app_utils_test.py
	coverage report -m

FLASKSOURCES=${APP}/flask_main.py,${APP}/flask_view.py

unittest_flask:
	${COVERAGE_RUN} --source ${FLASKSOURCES} -m unittest discover -s tests/unit_flask -p '*_test.py'
	coverage report -m

# /tornado_main.py,${APP}/tornado_view.py
TORNADOSOURCES=${APP}

unittest_tornado:
	${COVERAGE_RUN} --source ${TORNADOSOURCES} -m tornado.testing discover -s tests/unit_tornado -p '*_test.py'
	coverage report -m

integrationtest:
	${VIRTUALENV_DIR}/bin/python tests/integration/db_health.py
	${COVERAGE_RUN} --source ${APP} -m unittest discover -s tests/integration -p '*_test.py'


# Documentation via raml file
docs:
	npm set progress=false
	npm install raml2html raml2md
	raml2html ${RAML}/documents_api.raml -o docs/documents_api.html
	raml2md ${RAML}/documents_api.raml -o docs/documents_api.md
	open docs/documents_api.html && open docs/documents_api.md


# run application and simulate calls
run-flask:
	${VIRTUALENV_DIR}/bin/python ramlficated_api/flask_main.py

flask-calls:
	http post :5000/documents < ${RAML}/data/document-example.json
	http post :5000/documents < ${RAML}/data/document-examples.json
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
	env/bin/python ramlficated_api/tornado_main.py

tornado-calls:
	http post :8888/documents < ${RAML}/data/document-example.json
	http post :8888/documents < ${RAML}/data/document-examples.json
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

# Clean up everything
clean:
	rm -fv .DS_Store .coverage
	rm -rfv .cache
	find ${APP} -name '*.pyc' -exec rm -fv {} \;
	find ${APP} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf *.egg-info logs/*.log docs/*.html docs/*.md
	rm -Rf env tests/**/__pycache__ node_modules

release:
	python setup.py sdist register upload
