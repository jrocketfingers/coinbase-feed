import asyncio
import json
import os
from dataclasses import dataclass
from decimal import Decimal
from collections import defaultdict
from typing import Dict, Optional

import websockets

from coinbase_feed.vwap import VWAPFrame, Datapoint
from coinbase_feed.symbol import Symbol
from coinbase_feed.utils import load_config, instantiate_symbols


symbols: Optional[Dict[str, Symbol]] = None


async def run():
    async with websockets.connect("wss://ws-feed.pro.coinbase.com") as websocket:
        request = {
            "type": "subscribe",
            "product_ids": list(symbols.keys()),
            "channels": [
                "matches",
            ],
        }
        await websocket.send(json.dumps(request))

        try:
            async for raw_message in websocket:
                message = json.loads(raw_message)
                if message["type"] == "match":
                    await consumer(message)
        except KeyboardInterrupt:
            print("IMPLEMENT CORRECT CONNECTION CLOSING")


async def consumer(message):
    id_ = message["product_id"]
    datapoint = Datapoint(size=message["size"], price=message["price"])

    symbol = symbols[id_]
    symbol.vwap.add_datapoint(datapoint)

    vwap_value = symbol.vwap().quantize(symbol.quoting_precision)

    print(f"{id_}: {vwap_value}")


if __name__ == "__main__":
    config = load_config()
    symbols = instantiate_symbols(config)
    asyncio.run(run())
