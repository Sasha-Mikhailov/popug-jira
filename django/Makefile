install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml

dev-deps: deps
	pip-compile --resolver=backtracking --extra=dev --output-file=dev-requirements.txt pyproject.toml

fmt:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .

lint:
	dotenv-linter src/app/.env.ci
	cd src && ./manage.py check
	flake8 src
	cd src && mypy

test:
	mkdir -p src/static
	cd src && ./manage.py makemigrations --dry-run --no-input --check
	cd src && ./manage.py compilemessages
	cd src && pytest --dead-fixtures
	cd src && pytest -x

pr: fmt lint test

migration_name ='yet_another_migration'

migrations:
	cd src && ./manage.py makemigrations --name ${migration_name}

dry-migrations:
	cd src && ./manage.py makemigrations --dry-run

migrate: migrations
	cd src && ./manage.py migrate

run:
	cd src && ./manage.py runserver

shell:
	cd src && ./manage.py shell

topic = ''
clear-topic:
	docker exec broker /bin/kafka-topics --bootstrap-server 'localhost:9092' --delete --topic ${topic}
