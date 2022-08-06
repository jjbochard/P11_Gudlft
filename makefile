test:
	python -c 'import utils; utils.copy_clubs_to_test()'
	python -c 'import utils; utils.copy_competitions_to_test()'
	pytest --cov=. tests
	python -c 'import utils; utils.copy_test_to_clubs()'
	python -c 'import utils; utils.copy_test_to_competitions()'

coverage:
	coverage html
