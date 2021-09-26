Running
-------

Ensure you have `poetry` available:
```python
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

Configure `symbol_config.json` to your liking. The one provided in the repo is configured to support the requested symbols.

```python
poetry install
poetry run python coinbase_feed/main.py
```

Testing
-------

```python
poetry run pytest
```
