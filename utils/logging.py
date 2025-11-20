import logging

def get_logger():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/bot.log"),
        ]
    )
    return logging.getLogger("bot")