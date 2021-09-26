import asyncio
import json
from collections import defaultdict
from typing import Dict

from websockets import connect

from coinbase_feed.vwap import VWAPFrame


symbol_map: Dict[str, VWAPFrame] = defaultdict(VWAPFrame)


# example match:
# {"type":"match","trade_id":160338853,"maker_order_id":"3171b8a0-fb5c-404e-8a56-4dcc877a8cbd","taker_order_id":"623ed97b-28f2-4e30-bf5a-a6e5d02dc2ff","side":"sell","size":"0.18612113","price":"2955.29","product_id":"ETH-USD","sequence":21147999039,"time":"2021-09-26T10:52:44.866843Z"}


async def run():
    async with connect('wss://ws-feed.pro.coinbase.com') as websocket:
        request = {
            "type": "subscribe",
            "product_ids": [
                "BTC-USD",
                "ETH-USD",
                "ETH-BTC"
            ],
            "channels": [
                "matches",
            ]
        }
        await websocket.send(json.dumps(request))

        data = await websocket.recv()

        async for message in websocket:
            await consumer(message)

        print(data)


async def consumer(data):
    print(data)

asyncio.run(run())
