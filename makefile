test:
	python -c 'import utils; utils.copy_file_a_to_file_b("clubs.json", "tests/files_test/test_clubs.json")'
	python -c 'import utils; utils.copy_file_a_to_file_b("competitions.json", "tests/files_test/test_competitions.json")'
	pytest --cov-config=.coveragerc --cov=. tests
	python -c 'import utils; utils.copy_file_a_to_file_b("tests/files_test/test_clubs.json", "clubs.json")'
	python -c 'import utils; utils.copy_file_a_to_file_b("tests/files_test/test_competitions.json", "competitions.json")'

coverage:
	coverage html

functional:
	pytest tests/tests_functional/tests_functional.py -s
