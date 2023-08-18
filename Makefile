run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf achievement_api.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./achievement_api
	isort ./achievement_api
	black ./achievement_api

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-achievement_api postgres:15

migrate:
	alembic upgrade head
