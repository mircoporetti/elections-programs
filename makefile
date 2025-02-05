# Ensure Poetry dependencies are installed and check the environment variables
check_env:
	@echo "Ensuring Poetry dependencies are installed..."
	@poetry install
	@echo "Sourcing .env file..."
	@if [ -f .env ]; then \
		export $$(cat .env | xargs); \
		if [ -z "$$AWS_ACCESS_KEY_ID" ]; then \
        			echo "Error: AWS_SECRET_ACCESS_KEY is not set in the .env file."; \
        			exit 1; \
        		fi; \
		if [ -z "$$AWS_SECRET_ACCESS_KEY" ]; then \
			echo "Error: AWS_SECRET_ACCESS_KEY is not set in the .env file."; \
			exit 1; \
		fi; \
		if [ -z "$$API_USERNAME" ]; then \
			echo "Error: API_USERNAME is not set in the .env file."; \
			exit 1; \
		fi; \
		if [ -z "$$API_PASSWORD" ]; then \
			echo "Error: API_PASSWORD is not set in the .env file."; \
			exit 1; \
		fi; \
	else \
		echo "Error: .env file not found."; \
		exit 1; \
	fi

# Run FastAPI app
run: check_env
	@echo "Running FastAPI app..."
	env $$(cat .env | xargs) poetry run uvicorn src.webapp.main:app --reload

# Run pytest tests
test: check_env
	@echo "Running tests with pytest..."
	env $$(cat .env | xargs) poetry run pytest
