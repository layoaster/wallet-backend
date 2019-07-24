ARG PGSQL_VERSION=11.2

FROM postgres:${PGSQL_VERSION}

LABEL maintainer="Lionel Mena <lionelmena@gmail.com>"

WORKDIR /docker-entrypoint-initdb.d

COPY *.sh ./
