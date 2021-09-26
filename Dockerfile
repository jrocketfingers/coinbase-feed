FROM python:3.9

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH="$PATH:/root/.local/bin/"

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

COPY . /opt/service/

WORKDIR /opt/service/
CMD PYTHONPATH=/opt/service python /opt/service/coinbase_feed/main.py
