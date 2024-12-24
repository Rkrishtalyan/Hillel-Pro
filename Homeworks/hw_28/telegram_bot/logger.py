import logging
from logging.handlers import RotatingFileHandler

# ---- Configure Logging Levels ----
logging.getLogger().setLevel(logging.WARNING)

logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.ext').setLevel(logging.WARNING)

# ---- Configure Weather Bot Logger ----
logger = logging.getLogger('weather_bot')
logger.setLevel(logging.INFO)

# ---- Configure Rotating File Handler ----
handler = RotatingFileHandler(
    'app.log',
    maxBytes=5 * 1024 * 1024,  # 5 MB per log file
    backupCount=5              # Keep up to 5 backup log files
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# ---- Add Handler to Logger ----
logger.addHandler(handler)
