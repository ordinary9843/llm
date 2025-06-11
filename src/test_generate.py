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

        # Result
        # {
        #     "prompt": "給我一段 100 個字的柴犬總統大選故事",
        #     "generated_text": "在一個被愛與和平充滿的城市裡，住著一位名叫「柴柴」的小柴犬。他一直夢想成為城市的下一任領導者——柴犬總統。\n\n柴柴從小就熱愛運動和玩耍，特別喜歡跑步和追蹤球。他的目標是讓更多的人知道他的存在，並成為一個受歡迎的人物。\n\n然而，當柴柴決定參加市長大選時，他面臨了前所未有的挑戰。柴犬市政府的職員們都對柴柴抱有極大的疑慮，認為他是個新興的威脅。但是，柴柴不為所動，堅持自己可以治理城市，並帶領它走向美好的未來。\n\n經過激烈的競選活動，柴柴獲得了許多支持者的票，但他必須面對的挑戰也不少。柴犬市政府的職員開始對柴柴的行為感到不安，擔心他們的權力可能會受到威脅。\n\n最終，在一次重要的市政會議上，柴柴成功地展現了他的領導才能和決策能力。他不僅解決了市內的一系列問題，還鼓勵市民一起工作，共同創造美好未來。\n\n柴柴通過他的行動，證明了他有能力成為一個好的領導者。他的故事激励了许多人，讓他們相信只要有一顆勇往直前的心，就一定能夠克服任何困難。最终，柴柴在大選中获胜，成为了柴犬市的新市长。",
        # }
    except Exception as e:
        logger.error(f"Request failed: {e}")
