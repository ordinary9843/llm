import requests

from config import Config
from logger import logger


if __name__ == "__main__":
    config = Config()
    url = f"{config.endpoint}/v1/chat/completions"
    payload = {"messages": [{"role": "user", "content": "將 '柴犬' 翻譯成日文"}]}
    try:
        response = requests.post(url, json=payload)
        logger.info("Chat request successful")
        logger.info(f"Result: {response.json()['choices'][0]['message']['content']}")
    except Exception as e:
        logger.error(f"Request failed: {e}")
