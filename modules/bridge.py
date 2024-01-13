from .token_amount import TokenAmount
from .account import Account, AccountInfo

from utils.helpers import retry
from utils.config import (
    BRIDGE_CONTRACT
)
from utils.constants import Status


class Bridge(Account):
    def __init__(self, account_info: AccountInfo, to_chain):
        super().__init__(account_info)
        self.to_chain = to_chain
    
    @retry
    async def bridge_native_token(self, amount):        
        try:            
            contract = self.get_contract(BRIDGE_CONTRACT)
            
            tx_data = await self._get_tx_data(contract, amount)
            
            signed_tx = self.sign_tx(tx_data)   
            tx_hash = await self.send_raw_transaction(signed_tx)          
            
            status = await self.wait_until_tx_finished(tx_hash, f"Successfully sent {amount}{self.token} to {self.to_chain}!", Status.BRIDGED)
            
            return status
        except Exception as e:             
            self.logger.log_message(Status.ERROR, f"{self.chain} | Error while bridging: {e}")
            
            return False
    
    async def _get_tx_data(self, contract_address: str, value):
        var1 = '1'
        var2 = '40'
        data = (
            f'0xb1a1a882'
            f'{var1:0>64}'
            f'{var2:0>64}'
            + '0' * 64
        )
        
        try:
            gas_price = self.set_gas_price()
            nonce = await self.get_nonce()
            amount_wei = TokenAmount(value).Wei
            
            tx_data = {
                'from': self.address,
                'to': contract_address,
                'gasPrice': gas_price,
                'nonce': nonce,
                'data': data,
                'value': amount_wei,
                'chainId': self.chain_id
            }
            
            return tx_data            
        except Exception as e:
            self.logger.log_message("ERROR", f'Error while preparing transaction data: {e}')
            return None
                