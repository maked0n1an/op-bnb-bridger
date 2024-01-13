import sys

from loguru import logger
from utils.constants import Status


class Logger:
    def __init__(self, wallet_name: str, address: str):
        self.wallet_name = wallet_name
        self.address = address
        self.logger = logger
    
    def log_message(self, status: str, message: str):
        self.logger.log(status, f"{self.wallet_name: <5} | {self.address} | {message}")
    
    @classmethod
    def setup_logger_for_output(cls):
        logger.remove()
        logger.add(
            sys.stderr,
            format="<white>{time: DD/MM/YYYY HH:mm:ss}</white> | <level>"
            "{level: <8}</level> | <white>{message}</white>"
        )
        logger.add(
            "main.log",
            format="<green>{time: DD/MM/YYYY HH:mm:ss}</green> | <level>"
            "{level: <8}</level> | <white>{message}</white>"
        )
        
        logger.level(Status.BRIDGED, no=333, color="<green>")
        logger.level(Status.FAILED, no=253, color="<red>") 
        logger.level(Status.DELAY, no=444, color="<white>")
        
        return logger   
        