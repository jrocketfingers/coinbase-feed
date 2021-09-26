from decimal import Decimal
from coinbase_feed.vwap import VWAPFrame


class Symbol:
    def __init__(
        self,
        id: str,
        base_precision=Decimal("2"),
        quoting_precision=Decimal("2"),
        vwap: VWAPFrame = None,
        **kwargs,
    ):
        self.id = id
        self.vwap = vwap or VWAPFrame()
        self.base_precision = Decimal("10") ** (-base_precision)
        self.quoting_precision = Decimal("10") ** (-quoting_precision)
