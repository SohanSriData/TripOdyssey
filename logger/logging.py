import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "app.log"

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2)
handler.setFormatter(formatter)

logger = logging.getLogger("ai_trip_planner")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_logger():
    return logger
