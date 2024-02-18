import logging
import logging.handlers
import os
import requests
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Change the time to Central
ct_timezone = timezone(timedelta(hours=-6))

logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S %Z")
formatter.converter = lambda *args: datetime.now(ct_timezone).timetuple()
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://weather.talkpython.fm/api/weather?city=Chicago&country=US')
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f'Weather in Chicago: {temperature}')