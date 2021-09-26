from collections import deque
from dataclasses import dataclass
from decimal import Decimal
from typing import Deque, Optional, cast


class Datapoint:
    size: Decimal
    price: Decimal

    def __init__(self, size, price):
        self.size = Decimal(size)
        self.price = Decimal(price)


class VWAPFrame:
    maxlen: int
    datapoints: Deque[Datapoint]
    value_sum: Decimal  # value = size * price
    quantity_sum: Decimal

    def __init__(
        self,
        initial_data: Optional[Deque[Datapoint]] = None,
        maxlen: int = 200,
    ):
        if initial_data is not None:
            self.datapoints = initial_data
            if initial_data.maxlen is not None:
                self.maxlen = initial_data.maxlen
            else:
                self.maxlen = maxlen
        elif maxlen is not None:
            self.datapoints = deque(maxlen=maxlen)
            self.maxlen = maxlen

        self.value_sum = cast(Decimal, sum([d.size * d.price for d in self.datapoints]))
        self.quantity_sum = cast(Decimal, sum([d.size for d in self.datapoints]))

    def add_datapoint(self, new_datapoint: Datapoint):
        old_datapoint = Datapoint(size=0, price=0)
        if len(self.datapoints) >= self.maxlen:
            old_datapoint = self.datapoints.popleft()

        self.datapoints.append(new_datapoint)
        self.value_sum += (
            new_datapoint.price * new_datapoint.size
            - old_datapoint.price * old_datapoint.size
        )
        self.quantity_sum += new_datapoint.size - old_datapoint.size

    def __call__(self):
        return self.value_sum / self.quantity_sum
