.PHONY: docs

docs:
	raml2html ramls/books.raml -o docs/books.html
	open docs/books.html

calls:
	http post :5000/books title="Angel & Demons" authors:='["Dan Brown"]' id="1" views:=0
	http post :5000/books title="The Da Vinci Code" authors:='["Dan Brown"]' id="2" views:=0
	http post :5000/books authors:='["title missing but required"]' id="3"
	http :5000/books/1 -v
	http put :5000/books/1 script="ctx._source.views+=1"
	http put :5000/books/1 doc:='{"title": "Demons"}'
	http :5000/books/1 -v
	http delete :5000/books/2 -v
	# http delete :5000/books/1 -v

tree:
	ramlfications tree books.raml -v