install:
	uv sync

build:
	./build.sh

lint:
	uv run ruff check .

test:
	python -m coverage run --source='.' manage.py test
	python -m coverage report
	python -m coverage xml

.PHONY: test upload-coverage

migrate:
	uv run python manage.py makemigrations && \
	uv run python manage.py migrate

start-render:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000

make dev:
	uv run python manage.py runserver
