import asyncio
import random
import time
from typing import Any
from eth_typing import ChecksumAddress
from hexbytes import HexBytes

from web3 import AsyncWeb3, Web3
from web3.types import Wei
from web3.eth import AsyncEth
from web3.contract import Contract
from web3.exceptions import TransactionNotFound
from eth_account import Account as EthAccount

from .logger import Logger
from utils.config import CHAINS_DATA
from utils.constants import Status


class AccountInfo:
    def __init__(self, wallet_name: str, private_key: str, chain: str):
        self.wallet_name = wallet_name
        self.private_key = private_key
        self.chain = chain


class Account:
    def __init__(self, account_info: AccountInfo):
        self.wallet_name = account_info.wallet_name
        self.private_key = account_info.private_key        
        self.chain = account_info.chain        
        
        self.explorer = CHAINS_DATA[account_info.chain]['explorer']
        self.chain_id = CHAINS_DATA[account_info.chain]['chain_id']
        self.token = CHAINS_DATA[account_info.chain]['token']
        self.web3 = Web3(
            AsyncWeb3.AsyncHTTPProvider(random.choice(CHAINS_DATA[account_info.chain]["rpc"])),
            modules={'eth': (AsyncEth,)}, 
            middlewares=[],
        )
        self.account = EthAccount.from_key(account_info.private_key)
        self.address = self.account.address
        
        self.logger = Logger(self.wallet_name, self.address)
    
    def get_contract(self, contract_address: ChecksumAddress | str, abi: Any) -> Contract:
        contract_address = Web3.to_checksum_address(contract_address)
        
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        
        return contract
    
    async def get_nonce(self) -> int:
        nonce = await self.web3.eth.get_transaction_count(self.address)

        return nonce
    
    def set_gas_price(self) -> Wei:        
        gas_prices = {
            'bsc': '1',
            'op_bnb': '0.00002'
        }        
        gas_price = self.web3.to_wei(gas_prices[self.chain], 'gwei')
        
        return gas_price
    
    async def estimate_gas(self, contract_address: str, data: str | dict):
        estimate_gas = await self.web3.eth.estimate_gas({
            'to': contract_address,
            'data': data
        })
        
        return estimate_gas
    
    def sign_tx(self, tx_data):
        signed_tx = self.web3.eth.account.sign_transaction(tx_data, self.private_key)   
        
        return signed_tx           

    def sign_message(self, message):
        signed_message = self.web3.eth.account.sign_message(message, self.private_key)
        
        return signed_message
    
    async def send_raw_transaction(self, signed_tx) -> HexBytes:
        txn_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return txn_hash
    
    async def wait_until_tx_finished(self, tx_hash: HexBytes, message: str, message_status=Status.SUCCESS, max_wait_time=180) -> bool:
        start_time = time.time()

        while True:
            try:
                receipts = await self.web3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                
                if status == 1:
                    self.logger.log_message(message_status, f"{message} - {self.explorer}{tx_hash.hex()}")
                    
                    return True
                elif status is None:
                    await asyncio.sleep(1)
                else:
                    self.logger.log_message(Status.ERROR, f"{self.explorer}{tx_hash.hex()}")
                    
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    self.logger.log_message(Status.FAILED, f"Tx not found: {tx_hash.hex()}")
                    
                    return False
                await asyncio.sleep(1) 