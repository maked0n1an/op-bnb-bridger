import random
from modules import AccountInfo, Bridge
from settings.settings import (
    MIN_AMOUNT, 
    MAX_AMOUNT, 
    DECIMAL 
)


async def bridge(wallet_name, private_key, from_chain, to_chain) -> bool:
    '''
    Bridge BNB to/from opBNB chain
    
    chain - bsc | op_bnb
    '''
    min_amount = MIN_AMOUNT
    max_amount = MAX_AMOUNT
    decimal = DECIMAL   
    
    amount = round(random.uniform(min_amount, max_amount), decimal)
    
    account_info = AccountInfo(wallet_name, private_key, from_chain)    
    bridge = Bridge(account_info, to_chain)
        
    return await bridge.bridge_native_token(amount)      
        
        
        
    
     