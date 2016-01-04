.PHONY: docs

docs:
	raml2html ramls/articles-api.raml -o docs/articles-api.html
	open docs/articles-api.html

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

tree:
	ramlfications tree articles.raml -v