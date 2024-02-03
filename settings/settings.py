# Bridge:
#   from BSC to opBNB -> 'bsc'
#   from opBNB to BSC -> 'op_bnb' (not working)

# Do you want to use wallet names or generate ID's by program?
#   Use own names: True
#   Generate IDs: False
IS_ACCOUNT_NAMES = False

# Do you want to shuffle wallets?
IS_SHUFFLE_WALLETS = True

IS_SLEEP = True
SLEEP_FROM = 300 # secs
SLEEP_TO = 600 # secs

MIN_AMOUNT = 0.0002 # in BNB
MAX_AMOUNT = 0.0008 # in BNB

# How many decimals must be in float?
# For example, 
#     DECIMAL=3, so the bridged amount will be Y.XXX
#     DECIMAL=5, so the amount will be Y.XXXXX
#     DECIMAL=6, so the amount will be Y.XXXXXX
DECIMAL = 6

# How many retries will be executed if fail?
RETRY_COUNT = 3 