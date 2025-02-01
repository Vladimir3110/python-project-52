install:
	uv sync

lint:
	uv run ruff check .

build:
	./build.sh

dev:
	python manage.py runserver