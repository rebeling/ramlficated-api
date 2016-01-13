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
	raml2html ramls/articles-api.raml -o docs/articles-api.html
	raml2md ramls/articles-api.raml -o docs/articles-api.md
	open docs/articles-api.html && open docs/articles-api.md

calls:
	http post :5000/articles < data/article-example.json
	http post :5000/articles < data/article-examples.json
	http post :5000/articles id="42" note="500 on validation, missing fields"
	http :5000/articles/1 -v
	http put :5000/articles/1 script="ctx._source.views+=1"
	http put :5000/articles/1 doc:='{"title": "Demons"}'
	http :5000/articles/1 -v
	http delete :5000/articles/1 -v
	http delete :5000/articles/2 -v
	http delete :5000/articles/3 -v
	http delete :5000/articles/4 -v

tornado-calls:
	http post :8888/articles < data/article-example.json
	http post :8888/articles < data/article-examples.json
	http post :8888/articles id="42" note="500 on validation, missing fields"
	http :8888/articles/1 -v
	http put :8888/articles/1 script="ctx._source.views+=1"
	http put :8888/articles/1 doc:='{"title": "Demons"}'
	http :8888/articles/1 -v
	http delete :8888/articles/1 -v
	http delete :8888/articles/2 -v
	http delete :8888/articles/3 -v
	http delete :8888/articles/4 -v

tree:
	ramlfications tree articles.raml -v


clean:
	rm -fv .DS_Store .coverage
	rm -rfv .cache
	find ${APP_PATH} -name '*.pyc' -exec rm -fv {} \;
	find ${APP_PATH} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf *.egg-info logs/*.log docs/*.html docs/*.md
	rm -Rf env
