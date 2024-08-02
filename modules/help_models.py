from decimal import Decimal
from typing import Union


class NetworksNames:
    OP_BNB = 'op_bnb'
    BSC = 'bsc'


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = int(amount)
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals
        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals
        

class RawTxParams:
    def __init__(
        self,
        nonce: int,
        gas_price: int,
        amount: TokenAmount = None,
        multiplier_of_gas: float = None
    ):
        self.nonce = nonce
        self.gas_price = gas_price
        self.amount = amount
        self.multiplier_of_gas = multiplier_of_gas