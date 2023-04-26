gen:
	rm -f gen/*.py; cd proto; buf generate; cd ...
	
mongo: 
	docker run -d --name py-mongo -p 27017:27017 mongo  

dev:
	poetry run nodemon --exec python main.py

env:
	poetry shell

docker:
	docker build -t py-amibot .

.PHONY: gen, mongo, dev, env, docker

