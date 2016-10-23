.PHONY: flake8 demo test coverage dist publish

flake8:
	flake8

demo:
	python demo.py

run:
	waitress-serve --listen=127.0.0.1:8000 demo:application

dist:
	python setup.py sdist bdist_wheel

publish:
	python setup.py sdist bdist_wheel upload
