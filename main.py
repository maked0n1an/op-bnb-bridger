import asyncio
import random
import sys
import questionary

from questionary import Choice

from modules import Logger
from utils.config import (
    ACCOUNT_NAMES, 
    PRIVATE_KEYS,
)
from utils.helpers import delay, format_output
from settings.settings import (
    IS_ACCOUNT_NAMES,
    IS_SHUFFLE_WALLETS, 
    IS_SLEEP
)
from settings.modules_settings import *


def greetings():
    brand_label = "========== M A K E D 0 N 1 A N =========="
    name_label = "========= zkMessenger (via zkBridge) ========="
    
    print("")
    format_output(brand_label)
    format_output(name_label)

def is_bot_setuped_to_start():
    logger = Logger.setup_logger_for_output()
    end_bot = False

    if len(PRIVATE_KEYS) == 0:
        logger.error("Don't imported private keys in 'private_keys.txt'!")
        return end_bot
    if len(ACCOUNT_NAMES) == 0 and IS_ACCOUNT_NAMES:
        logger.error("Please insert names into account_names.txt")
        return end_bot
    if len(PRIVATE_KEYS) != len(ACCOUNT_NAMES) and IS_ACCOUNT_NAMES:
        logger.error(
            "The account names' amount must be equal to private keys' amount")
        return end_bot
    
    return True

def get_module_data():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Bridge from BSC to opBNB", [bridge, 'bsc', 'op_bnb']),
            # Choice("2) Bridge from opBNB to BSC", [bridge, 'op_bnb', 'bsc']),
            Choice("3) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        exit_label = "========= It's all! ========="
        format_output(exit_label)
        sys.exit()
    return result

def get_wallets():
    if IS_ACCOUNT_NAMES:
        wallets = [
            {
                "name": account_name,
                "key": key,
            } for account_name, key in zip(ACCOUNT_NAMES, PRIVATE_KEYS)
        ]
    else:
        wallets = [
            {
                "name": _id,
                "key": key,
            } for _id, key, in enumerate(PRIVATE_KEYS)
        ]    

    return wallets

async def run_module(module, wallet):
    if isinstance(module, list):
        module_function = module[0]
        return await module_function(wallet["name"], wallet["key"], *module[1:])
    elif callable(module):
        return await module(wallet["name"], wallet["key"])
    else:
        raise ValueError("Invalid module format")

async def main(module):  
    wallets = get_wallets()

    if IS_SHUFFLE_WALLETS:
        random.shuffle(wallets)
    
    for wallet in wallets:
        is_result = await run_module(module, wallet)
        
        if IS_SLEEP and wallet != wallets[-1] and is_result:
            await delay()        

if __name__ == '__main__':
    greetings()
    
    if not is_bot_setuped_to_start():
        exit_label = "========= The bot has ended it's work! ========="
        format_output(exit_label)
        sys.exit()
    
    module_data = get_module_data()
    
    asyncio.run(main(module_data))
    
    
        

