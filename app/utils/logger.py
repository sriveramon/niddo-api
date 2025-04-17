import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app_debug.log", mode="a"),  # Log to a file
    ],
)

# Create a logger instance
logger = logging.getLogger("niddo-api")