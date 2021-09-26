import os
import json
import tempfile
from decimal import Decimal

import pytest

from coinbase_feed.symbol import Symbol
from coinbase_feed.utils import load_config, instantiate_symbols


def test_default():
    # when a load is called with nothing set
    config = load_config()

    # then config should match what's in the default symbol_config.json in the repo
    # TODO: consider alternatives -- this is breaks in case someone actually wants to change the config
    assert config == [
        {
            "id": "BTC-USD",
            "base_precision": 8,
            "quoting_precision": 2
        },
        {
            "id": "ETH-USD",
            "base_precision": 18,
            "quoting_precision": 2
        },
        {
            "id": "ETH-BTC",
            "base_precision": 18,
            "quoting_precision": 8
        }
    ]


def test_config_file():
    # given a config file filled with test data
    data = {"henlo": "there"}
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        json.dump(data, f)

    # and SYMBOL_CONFIG_FILE is set
    os.environ["SYMBOL_CONFIG_FILE"] = path

    # when a load is called
    config = load_config()

    # then config should match the test data
    assert config == data


def test_config_from_env():
    data = {"henlo": "there"}

    os.environ["SYMBOL_CONFIG"] = json.dumps(data)

    config = load_config()

    assert config == data


def test_instantiate_symbols():
    # given a valid config
    config = [{"id": "BTC-USD", "base_precision": 10, "quoting_precision": 12}]

    # when instantiate is called
    symbols = instantiate_symbols(config)

    # then it should correctly instantiate a dictionary of symbols
    symbol = symbols["BTC-USD"]
    assert isinstance(symbol, Symbol)
    assert symbol.id == "BTC-USD"
    assert symbol.base_precision == Decimal("0.0000000001")
    assert symbol.quoting_precision == Decimal("0.000000000001")


def test_instantiate_symbols_with_invalid_config():
    config = [{"utter": "nonsense"}]

    with pytest.raises(Exception):
        instantiate_symbols(config)
