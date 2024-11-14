import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("log_file.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(mesage)s"
)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
