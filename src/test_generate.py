import requests

from config import Config
from logger import logger

if __name__ == "__main__":
    config = Config()
    url = f"{config.endpoint}/v1/generate"
    payload = {"prompt": "寫給我一段 100 個字的柴犬總統大選故事"}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info("Generation request successful")
        logger.info(f"Result: {response.json()}")
    except Exception as e:
        logger.error(f"Request failed: {e}")
