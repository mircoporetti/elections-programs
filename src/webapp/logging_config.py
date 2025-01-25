import logging


logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log"),  # Log to a file
    ],
)

logger = logging.getLogger(__name__)

# Configure Uvicorn and FastAPI loggers
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.INFO)
uvicorn_logger.propagate = True  # Propagate logs to the root logger

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.setLevel(logging.INFO)
fastapi_logger.propagate = True  # Propagate logs to the root logger