from web3.contract import Contract

from settings.settings import IS_TO_BRIDGE_FULL_BALANCE

from .token_amount import TokenAmount
from .account import Account, AccountInfo

from utils.helpers import retry
from utils.config import (
    BRIDGE_ABI,
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
            contract = self.get_contract(BRIDGE_CONTRACT, BRIDGE_ABI)

            tx_data = await self._get_tx_data(contract, amount)

            signed_tx = self.sign_tx(tx_data)
            tx_hash = await self.send_raw_transaction(signed_tx)

            status = await self.wait_until_tx_finished(tx_hash, f"Successfully sent {amount} {self.token} to {self.to_chain}!", Status.BRIDGED)

            return status
        except Exception as e:
            self.logger.log_message(
                Status.ERROR, f"{self.chain} | Error while bridging: {e}")

            return False

    async def _get_tx_data(self, contract: Contract, value):
        try:
            gas_price = await self.get_gas_price()
            nonce = await self.get_nonce()

            if IS_TO_BRIDGE_FULL_BALANCE:
                amount_wei = 1_000
                tx_data = await contract.functions.depositETH(1, '0x').build_transaction(
                    {
                        'from': self.address,
                        'nonce': nonce,
                        'gasPrice': gas_price,
                        'value': amount_wei
                    }
                )

                gas = tx_data['gas']
                balance = await self.get_balance()

                amount = TokenAmount(
                    balance.Wei - 100 * (gas * gas_price), 
                    wei=True
                )
            else:
                amount = TokenAmount(value)
                
            tx_data = await contract.functions.depositETH(1, '0x').build_transaction(
                {
                    'from': self.address,
                    'nonce': nonce,
                    'gasPrice': gas_price,
                    'value': amount.Wei
                }
            )

            return tx_data
        except Exception as e:
            self.logger.log_message(
                "ERROR", f'Error while preparing transaction data: {e}')
            return None
