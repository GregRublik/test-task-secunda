FROM python:3.12.4-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install --system .

COPY . .

ENV PYTHONPATH=/app/src

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
