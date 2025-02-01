install:
	uv sync

lint:
	uv run ruff check .

build:
	./build.sh

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

dev:
	python manage.py runserver

start-render:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
