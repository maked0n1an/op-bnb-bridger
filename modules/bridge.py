from typing import Tuple
from web3.contract import Contract
from web3.types import TxParams

from settings.settings import IS_TO_BRIDGE_FULL_BALANCE

from .help_models import RawTxParams, TokenAmount
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
    async def bridge_native_token(self, amount: float | int):
        try:
            contract = self.get_contract(BRIDGE_CONTRACT, BRIDGE_ABI)

            tx_data, bridge_amount = await self._get_tx_data(contract, amount)
            
            amount_to_log = round(bridge_amount.Ether, 5)

            signed_tx = self.sign_tx(tx_data)
            tx_hash = await self.send_raw_transaction(signed_tx)

            status = await self.wait_until_tx_finished(
                tx_hash, 
                f"Successfully sent {amount_to_log} {self.token} to {self.to_chain}!", 
                Status.BRIDGED
            )

            return status
        except Exception as e:
            self.logger.log_message(
                Status.ERROR, f"{self.chain} | Error while bridging: {e}")

            return False

    async def _get_tx_data(
        self, 
        contract: Contract, 
        amount: float | int
    ) -> Tuple[TxParams, TokenAmount]:
        try:
            raw_tx_params = RawTxParams(
                nonce = await self.get_nonce(),
                gas_price = await self.get_gas_price(),
                multiplier_of_gas=self.get_multiplier_of_gas()
            )
            
            if IS_TO_BRIDGE_FULL_BALANCE:
                raw_tx_params.amount = TokenAmount(100, wei=True)
                
                tx_params = await self.create_tx_data(contract, raw_tx_params)
                balance = await self.get_balance()

                raw_tx_params.amount = TokenAmount(
                    amount=(
                        balance.Wei - raw_tx_params.multiplier_of_gas * (
                            tx_params['gas'] * tx_params['gasPrice']
                        )
                    ),                    
                    wei=True
                )
            else:
                raw_tx_params.amount = TokenAmount(amount)
                
            tx_data = await self.create_tx_data(contract, raw_tx_params)

            return tx_data, raw_tx_params.amount
        except Exception as e:
            self.logger.log_message(
                "ERROR", f'Error while preparing transaction data: {e}')
            
        return None

    async def create_tx_data(
        self, 
        contract: Contract, 
        raw_tx_params: RawTxParams
    ) -> TxParams:
        return await contract.functions.depositETH(1, '0x').build_transaction(
            {
                'from': self.address,
                'nonce': raw_tx_params.nonce,
                'gasPrice': raw_tx_params.gas_price,
                'value': raw_tx_params.amount.Wei
            }
        )