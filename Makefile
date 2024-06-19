manage:
	docker-compose exec server python3 backend/manage.py $(filter-out $@,$(MAKECMDGOALS))

isort:
	docker-compose exec server isort backend

black:
	docker-compose exec server black backend

pip-install:
	docker-compose exec server pip3 install $(filter-out $@,$(MAKECMDGOALS))

pip-freeze:
	docker-compose exec server pip3 freeze > backend/requirements.txt

bash:
	docker-compose exec server bash
