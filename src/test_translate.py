import requests

from config import Config
from logger import logger

if __name__ == "__main__":
    config = Config()
    url = f"{config.endpoint}/v1/translate"
    payload = {"word": "柴犬", "languages": ["zh-TW", "en", "ja-JP"]}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info("Translation request successful")
        logger.info(f"Result: {response.json()}")
    except Exception as e:
        logger.error(f"Request failed: {e}")
