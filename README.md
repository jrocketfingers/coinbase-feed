Running
-------

![Test CI](https://github.com/jrocketfingers/coinbase-feed/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/gh/jrocketfingers/coinbase-feed/branch/master/graph/badge.svg?token=NOP89CO2WB)](https://codecov.io/gh/jrocketfingers/coinbase-feed)

Ensure you have `poetry` available:
```python
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

Configure `symbol_config.json` to your liking. The one provided in the repo is configured to support the requested symbols.

```python
poetry install
poetry run python coinbase_feed/main.py
```

Alternatively, you can run this in docker.
```
docker build -t coinbase-feed .
docker run --rm -it coinbase-feed
```

Since this is a toy, I didn't consider using an image registry.

Testing
-------

```python
poetry run pytest
```

Design considerations
---------------------

Given the nature of volume-weighted average price, we can avoid recalculations
of the entire window by maintaining a copy of `price x size` and `size` sums, as
well as a deque of datapoints. Each time a new match arrives we can subtract the
leftmost datapoint from sums, remove it from the deque, add the new datapoint to
the sums and add it to the right side of the deque. This way, we do not need to
iterate through the full window of datapoints each time a recalculation is
performed.

Since the VWAP represents prices, their precisions are in quoting currency
(usually the second instrument in the pair -- ETHBTC is quoted in BTC). These
precisions can be configured in `symbol_config.json`.
