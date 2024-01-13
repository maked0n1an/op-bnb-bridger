from .helpers import read_txt, load_json

ACCOUNT_NAMES = read_txt("input_data/account_names.txt")

PRIVATE_KEYS = read_txt("input_data/private_keys.txt")

CHAINS_DATA = load_json("data/chains_data.json")

BRIDGE_CONTRACT = "0xF05F0e4362859c3331Cb9395CBC201E3Fa6757Ea"