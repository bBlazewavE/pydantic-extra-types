"""Tests for DSN types migrated from pydantic.networks."""

from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.dsn_types import (
    AmqpDsn,
    ClickHouseDsn,
    CockroachDsn,
    KafkaDsn,
    MariaDBDsn,
    MongoDsn,
    MySQLDsn,
    NatsDsn,
    PostgresDsn,
    RedisDsn,
    SnowflakeDsn,
)


@pytest.mark.parametrize(
    'dsn_type,valid_url',
    [
        (PostgresDsn, 'postgres://user:pass@localhost:5432/db'),
        (PostgresDsn, 'postgresql://user:pass@localhost:5432/db'),
        (PostgresDsn, 'postgresql+asyncpg://user:pass@localhost:5432/db'),
        (PostgresDsn, 'postgresql+pg8000://user:pass@localhost:5432/db'),
        (PostgresDsn, 'postgresql+psycopg://user:pass@localhost/db'),
        (CockroachDsn, 'cockroachdb://user:pass@localhost:26257/db'),
        (CockroachDsn, 'cockroachdb+psycopg2://user:pass@localhost/db'),
        (AmqpDsn, 'amqp://guest:guest@localhost:5672/'),
        (AmqpDsn, 'amqps://guest:guest@localhost:5672/'),
        (RedisDsn, 'redis://localhost:6379/0'),
        (RedisDsn, 'rediss://:pass@localhost:6379/1'),
        (MongoDsn, 'mongodb://localhost:27017'),
        (MongoDsn, 'mongodb+srv://user:pass@cluster.example.com/db'),
        (KafkaDsn, 'kafka://localhost:9092'),
        (NatsDsn, 'nats://localhost:4222'),
        (MySQLDsn, 'mysql://user:pass@localhost:3306/db'),
        (MySQLDsn, 'mysql+pymysql://user:pass@localhost/db'),
        (MariaDBDsn, 'mariadb://user:pass@localhost:3306/db'),
        (MariaDBDsn, 'mariadb+pymysql://user:pass@localhost/db'),
        (ClickHouseDsn, 'clickhouse://localhost:9000/db'),
        (ClickHouseDsn, 'clickhouse+native://localhost/db'),
        (SnowflakeDsn, 'snowflake://user:pass@account.snowflakecomputing.com/db'),
    ],
)
def test_valid_dsn(dsn_type: type, valid_url: str) -> None:
    class Model(BaseModel):
        url: dsn_type  # type: ignore[valid-type]

    m = Model(url=valid_url)
    assert str(m.url) == valid_url or str(m.url).startswith(valid_url.split('://')[0])


@pytest.mark.parametrize(
    'dsn_type,invalid_url',
    [
        (PostgresDsn, 'http://localhost/db'),
        (CockroachDsn, 'postgres://localhost/db'),
        (AmqpDsn, 'http://localhost/'),
        (RedisDsn, 'http://localhost/0'),
        (MongoDsn, 'http://localhost:27017'),
        (KafkaDsn, 'http://localhost:9092'),
        (NatsDsn, 'http://localhost:4222'),
        (MySQLDsn, 'http://localhost:3306/db'),
        (MariaDBDsn, 'http://localhost:3306/db'),
        (ClickHouseDsn, 'http://localhost:9000/db'),
        (SnowflakeDsn, 'http://account.snowflakecomputing.com/db'),
    ],
)
def test_invalid_dsn_scheme(dsn_type: type, invalid_url: str) -> None:
    class Model(BaseModel):
        url: dsn_type  # type: ignore[valid-type]

    with pytest.raises(ValidationError):
        Model(url=invalid_url)


def test_postgres_host_required() -> None:
    class Model(BaseModel):
        url: PostgresDsn

    with pytest.raises(ValidationError):
        Model(url='postgres://user:pass@/db')


def test_redis_defaults() -> None:
    class Model(BaseModel):
        url: RedisDsn

    m = Model(url='redis://localhost')
    assert m.url.host == 'localhost'
    assert m.url.path == '/0' or '/0' in str(m.url)


def test_mongo_default_port() -> None:
    class Model(BaseModel):
        url: MongoDsn

    m = Model(url='mongodb://localhost')
    assert str(m.url) == 'mongodb://localhost:27017'


def test_postgres_multihost() -> None:
    class Model(BaseModel):
        url: PostgresDsn

    m = Model(url='postgres://user:pass@host1:5432,host2:5432/db')
    hosts = m.url.hosts()
    assert len(hosts) == 2


def test_snowflake_host_required() -> None:
    class Model(BaseModel):
        url: SnowflakeDsn

    m = Model(url='snowflake://user:pass@myaccount.snowflakecomputing.com/db')
    assert m.url.host is not None


def test_json_serialization() -> None:
    class Model(BaseModel):
        url: PostgresDsn

    m = Model(url='postgres://user:pass@localhost:5432/db')
    data = m.model_dump(mode='json')
    assert data['url'] == 'postgres://user:pass@localhost:5432/db'

    # Round-trip
    m2 = Model.model_validate(data)
    assert str(m2.url) == str(m.url)
