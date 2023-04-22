gen:
	rm -f gen/*.py; cd proto; buf generate; cd ...
	
mongo: 
	docker run -d --name py-mongo mongo    

PHONY: gen, mongo