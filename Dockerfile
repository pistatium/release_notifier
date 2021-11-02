FROM python:3.9-slim
WORKDIR /opt/checker
RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/checker
RUN poetry install --no-root

ADD checker.py /opt/checker/checker.py
CMD python -u checker.py
