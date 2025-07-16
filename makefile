.PHONY: install test coverage report clean

install:
	pip install -r requirements.txt

test:
	python -m pytest -v

test-coverage:
	python -m pytest --cov=. --cov-report=html --cov-report=term-missing

coverage: test-coverage

report:
	coverage report
	coverage html

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf data/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
