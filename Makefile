gen:
	rm -f gen/*.py; cd proto; buf generate; cd ...
	
PHONY: gen