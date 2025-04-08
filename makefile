.PHONY: install test coverage report clean

install:
	pip install -r requirements.txt
	pip install pytest coverage

test:
	coverage run --source=api,models,db,utils -m pytest

report:
	coverage report
	coverage html
	open htmlcov/index.html

coverage: test report

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
