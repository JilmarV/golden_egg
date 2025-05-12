run-test:
	@docker-compose exec fastapi bash -c "cd /app && pytest -v"

validate-pylint:
	@pylint FastAPI/app/