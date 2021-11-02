FROM python:3.9-slim
WORKDIR /opt/checker
RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/checker
RUN poetry install --no-root

COPY checker.py notifier.py /opt/checker
CMD python -u checker.py
