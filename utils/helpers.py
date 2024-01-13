import asyncio
import json
import random

from pathlib import Path
from loguru import logger

from settings.settings import (
    RETRY_COUNT, 
    SLEEP_FROM, 
    SLEEP_TO
)
from utils.constants import Status


def read_txt(filepath: Path | str):
    with open(filepath, 'r') as file:
        return [row.strip() for row in file]
    
def load_json(filepath: Path | str):
    with open(filepath, 'r') as file:
        return json.load(file)

def format_output(message: str):
    print(f"{message:^80}")
    
def retry(func):
    async def _wrapper(*args, **kwargs):
        retries = 1
                  
        while retries <= RETRY_COUNT:                
            try:  
                result = await func(*args, **kwargs)
                
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                await delay(10, 30, f"One more retry: {retries}/{RETRY_COUNT}")
                retries += 1
        
    return _wrapper
    
    
async def delay(sleep_from :int = SLEEP_FROM, sleep_to :int = SLEEP_TO, message: str =""):
    delay_secs = random.randint(sleep_from, sleep_to)
    logger.log(Status.DELAY, f"{message} - waiting for {delay_secs}")
    await asyncio.sleep(delay_secs)