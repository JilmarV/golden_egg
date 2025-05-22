run-test:
	@docker-compose exec golden_egg-api-1 bash -c "cd /app && pytest -v"

validate-pylint:
	@pylint FastAPI/app/