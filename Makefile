gen:
	rm -f gen/*.py; cd proto; buf generate; cd ...
	
mongo: 
	docker run -d --name py-mongo -p 27017:27017 mongo    

PHONY: gen, mongo