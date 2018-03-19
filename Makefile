init:
	pip install -r requirements.txt

test:
	python -m unittest test_mock_requests.py

.PHONY: init test
