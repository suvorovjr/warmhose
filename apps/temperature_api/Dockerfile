FROM python:3.13-slim-bookworm AS builder

WORKDIR /app

RUN pip config --user set global.index-url https://pypi-mirror.gitverse.ru/simple/

RUN pip install --no-cache-dir uv~=0.9

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

FROM python:3.13-slim-bookworm AS runtime

RUN groupadd --gid 1001 web && \
    useradd --uid 1001 --gid web --no-create-home web

WORKDIR /app

COPY --from=builder --chown=web:web /app/.venv /app/.venv

COPY --chown=web:web . .

COPY entrypoint.sh /web/entrypoint.sh
RUN chmod +x /web/entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"

USER web

ENTRYPOINT ["/web/entrypoint.sh"]