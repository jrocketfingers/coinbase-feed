import asyncio
import json
import os

import websockets

from coinbase_feed.vwap import Datapoint
from coinbase_feed.utils import load_config, instantiate_symbols


ws_url = os.getenv("WS_URL", "wss://ws-feed.pro.coinbase.com")


async def run(symbols):
    async with websockets.connect(ws_url) as websocket:
        request = {
            "type": "subscribe",
            "product_ids": list(symbols.keys()),
            "channels": [
                "matches",
            ],
        }
        await websocket.send(json.dumps(request))

        async for raw_message in websocket:
            message = json.loads(raw_message)
            if message["type"] == "match":
                await consumer(message, symbols)


async def consumer(message, symbols):
    id_ = message["product_id"]
    datapoint = Datapoint(size=message["size"], price=message["price"])

    symbol = symbols[id_]
    symbol.vwap.add_datapoint(datapoint)

    vwap_value = symbol.vwap().quantize(symbol.quoting_precision)

    send_to_output_stream(id_, vwap_value)


def send_to_output_stream(id_, vwap_value):
    print(f"{id_}: {vwap_value}")


if __name__ == "__main__":
    config = load_config()
    symbols = instantiate_symbols(config)
    asyncio.run(run(symbols))
