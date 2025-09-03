.PHONY: test install clean run

install:
	pip install pytest

test:
	pytest

run:
	python significance.py sample_data.json

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name '*.pyc' -delete
