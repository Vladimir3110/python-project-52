install:
	uv sync

lint:
	uv run ruff check .

build:
	./build.sh

dev:
	python manage.py runserver

start-render:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
