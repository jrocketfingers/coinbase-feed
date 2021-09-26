import asyncio
import json
import random
from decimal import Decimal
from unittest.mock import call

import pytest
import websockets

from coinbase_feed.main import run
from coinbase_feed.symbol import Symbol


@pytest.fixture
def symbols():
    return {
        "ETH-USD": Symbol(
            id="ETH-USD", base_precision=Decimal("2"), quote_precision=Decimal("2")
        )
    }


@pytest.mark.asyncio
async def test_with_fake_websocket_server(mocker, symbols):
    """
    Creates a stream of fake data served by a fake websocket server. Once the full stream is sent
    it verifies that the output data matches a naive calculation of VWAP.

    TEST_SIZE controls the amount of matches sent. A number above 200 (or whatever the maxlen is set to)
    will ensure that the window sliding is actually tested.
    """
    # given an output mock
    output_mock = mocker.patch("coinbase_feed.main.send_to_output_stream")

    # and a ws path pointing to a fake server
    mocker.patch("coinbase_feed.main.ws_url", "ws://localhost:34568")

    done = asyncio.Future()

    TEST_SIZE = 400
    # and a random dataset
    data = [
        {
            "size": random.randint(1, 5000) / 1000,
            "price": random.randrange(3000, 60000),
        }
        for i in range(TEST_SIZE)
    ]

    async def handler(websocket, path):
        try:
            await websocket.recv()

            for datum in data:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "match",
                            "product_id": "ETH-USD",
                            "size": datum["size"],
                            "price": datum["price"],
                        }
                    )
                )

            # then the output stream should be called with
            done.set_result(True)
        except Exception as err:
            done.set_exception(err)

    # when we run a fake websocket server
    async with websockets.serve(handler, "localhost", 34568):
        # and run the client
        await asyncio.gather(
            asyncio.create_task(run(symbols)),
            asyncio.wait_for(done, timeout=5),
        )

        calls = []

        # then the calls to the output stream should match the VWAP naively calculated from the dataset
        WINDOW_SIZE = 200
        for i in range(0, TEST_SIZE):
            start = max(0, i + 1 - WINDOW_SIZE)
            end = i + 1

            value_sum = sum([Decimal(d["price"]) * Decimal(d["size"]) for d in data[start:end]])
            size_sum = sum([Decimal(d["size"]) for d in data[start:end]])
            vwap = Decimal(value_sum / size_sum).quantize(Decimal("0.01"))
            calls.append(call("ETH-USD", vwap))

        output_mock.assert_has_calls(calls)
