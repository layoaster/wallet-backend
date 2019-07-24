ARG PYTHON_VERSION=3.7.2-alpine3.9

# Python base image
FROM python:${PYTHON_VERSION} AS python37-base

LABEL maintainer="Lionel Mena <lionelmena@gmail.com>"

WORKDIR /wheels

COPY requirements.txt requirements_dev.txt ./

RUN set -x \
    && apk add --no-cache --virtual build-dependencies \
        g++ \
        libffi-dev \
        postgresql-dev \
    # Generating wheels
    && pip install --upgrade pip \
    && pip wheel -r /wheels/requirements_dev.txt \
    # Cleaning up image
    && rm -rf /root/.cache \
    && apk del build-dependencies



# Development image
FROM python:${PYTHON_VERSION} AS wallet-backend-dev

LABEL maintainer="Lionel Mena <lionelmena@gmail.com>"

COPY --from=python37-base /wheels /wheels

RUN set -x \
    && apk add --no-cache \
        libpq \
    # Installing dependencies
    && pip install --upgrade pip \
    && pip install -r /wheels/requirements_dev.txt -f /wheels \
    # Cleaning up image
    && rm -rf /wheels \
    && rm -rf /root/.cache

WORKDIR /code

COPY . ./

CMD [ "gunicorn", "-c", "./etc/gunicorn_conf_dev.py", "wallet_api.wsgi:app" ]



# Production image
FROM python:${PYTHON_VERSION} AS wallet-backend-prod

LABEL maintainer="Lionel Mena <lionelmena@gmail.com>"

COPY --from=python37-base /wheels /wheels

RUN set -x \
    && apk add --no-cache \
        libpq \
        shadow \
    # Installing dependencies
    && pip install --upgrade pip \
    && pip install -r /wheels/requirements.txt -f /wheels \
    # Cleaning up image
    && rm -rf /wheels \
    && rm -rf /root/.cache \
    # Required directories structure
    && mkdir -p /code/wallet_api /code/tests

RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup --create-home appuser
USER appuser

WORKDIR /home/appuser

COPY --chown=appuser:appgroup ./wallet_api/ ./wallet_api/
COPY --chown=appuser:appgroup ./tests/ ./tests/
COPY --chown=appuser:appgroup ./etc/gunicorn_conf_prod.py .coveragerc  pytest.ini  ./

ENTRYPOINT [ "gunicorn" ]
CMD [ "-c", "./gunicorn_conf_prod.py", "wallet_api.wsgi:app" ]
