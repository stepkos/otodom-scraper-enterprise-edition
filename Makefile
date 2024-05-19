manage:
	docker-compose exec server python3 backend/manage.py $(filter-out $@,$(MAKECMDGOALS))
