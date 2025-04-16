install:
	uv sync

build:
	./build.sh

lint:
	uv run ruff check .

test:
	coverage run --source='.' manage.py test
	coverage report
	coverage xml

upload-coverage:
	curl -L https://qlty.sh/upload -o upload
	chmod +x upload
	bash./upload --token $${QLTY_TOKEN} --format coverage.xml

.PHONY: test upload-coverage

migrate:
	uv run python manage.py makemigrations && \
	uv run python manage.py migrate

start-render:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000

make dev:
	uv run python manage.py runserver
