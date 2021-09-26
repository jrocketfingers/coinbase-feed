import json
import os
from typing import List, Dict

from coinbase_feed.symbol import Symbol


def load_config() -> List[Symbol]:
    """
    Loads the symbols from environment or a file.

    Checks SYBMOL_CONFIG env var for a raw json string,
    then SYMBOL_CONFIG_FILE for a file path,
    finally it attempts to load 'symbol_config.json' at the root of the package.
    """
    config_string = os.getenv("SYMBOL_CONFIG")

    if config_string is not None:
        config = json.loads(config_string)
    else:
        config_file = os.getenv("SYMBOL_CONFIG_FILE")

        if config_file is None:
            config_file = "symbol_config.json"

        with open(config_file) as f:
            config = json.load(f)

    return config


def instantiate_symbols(config: List) -> Dict[str, Symbol]:
    symbols = {}

    for data in config:
        try:
            symbols[data["id"]] = Symbol(**data)
        except TypeError as e:
            raise Exception(f"Couldn't instantiate a symbol <{data}> with the error '{e}'")

    return symbols
