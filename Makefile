build:
	docker compose build
build-no-cache:
	docker compose build --no-cache
test:
	docker compose build tests && docker compose run --rm tests
run:
	docker compose run tests bash
black:
	docker compose run base_build bash -c 'black .'
format:
	docker compose run base_build bash -c 'black . && flake8 --ignore=E,W .'
sort-imports:
	docker compose run base_build bash -c 'isort . --profile "black"'
mypy:
	docker compose run base_build bash -c 'cd .. && mypy .'
pip-compile:
	docker compose run --rm base_build bash -c 'cd /project && pip install uv && uv pip compile --output-file=requirements.txt requirements.in'