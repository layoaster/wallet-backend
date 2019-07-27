# Wallets Manager

Proof-of-concept of a REST API for a money-transferring service.

## Description

The service, at its most basic, should allow the following operations:

* Check the current balance of an user.
* Money transfer between users.


## Usage

A `Makefile` is available so you can use `make` to:

```
build      Builds app containers
start      Gets app containers up & running
stop       Stop and removes app containers
logs       Fetches active containers logs
test       Runs the app suite of tests
migrate    Applies database migrations
check      Checks code's quality & style [flake8 and black]
format     Runs 'black' to format code
clean      remove temporary/cache/unnecesary files
```

Before running the app you must create a `.env` file to **configure** it. It should contain the
following:

```shell
FLASK_SECRET_KEY=<secret-key>
PSQL_CLIENT_HOST=wallet-backend-db
PSQL_CLIENT_DATABASE=<database-name>
PSQL_CLIENT_USERNAME=<database-user>
PSQL_CLIENT_PASSWORD=<database-password>
```


## Requirements

The following is required to run/develop the service:

* Docker
* docker-compose (v18.06.0+)
* GNU Make


## API

For simplicity the REST API has only the `user` resource.

### Create a new user

```shell
POST /user
```
**Body**

Parameter | Type | Description
--------- | ---- | -----------
`name` | str | User name
`email` | str | User email
`init_balance` | str | Initial amount of money (Optional: defaults to `0.0`)

**Response's status codes**

Code | Description
---- | -----------
201 | User successfully created
400 | Bad request (invalid input data)
403 | User already exists

### Check user's balance:

```shell
GET /user/{id}/balance
```
**Response's status codes**

Code | Description
---- | -----------
200 | Transfer successfully made
403 | User not found (invalid user ID)

### Make a transfer

```shell
POST /user/{id}/transfer
```
**Body**

Parameter | Type | Description
--------- | ---- | -----------
`toUserId` | int | User ID of the transfer recipient
`amount` | str | amount of money to transfer (max two decimals)

**Response's status codes**

Code | Description
---- | -----------
200 | Transfer successfully made
400 | Bad request (invalid input data)
403 | Insufficient funds / Invalid user ID


## TODO:

1. Improve tests coverage.
2. Write a proper API documentation.
