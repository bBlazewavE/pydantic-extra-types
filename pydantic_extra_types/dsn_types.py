"""DSN (Data Source Name) types for various databases and messaging systems.

These types were migrated from `pydantic.networks` as part of
https://github.com/pydantic/pydantic/issues/9071.
"""

from __future__ import annotations

from pydantic import AnyUrl, UrlConstraints
from pydantic.networks import _BaseMultiHostUrl

__all__ = [
    'PostgresDsn',
    'CockroachDsn',
    'AmqpDsn',
    'RedisDsn',
    'MongoDsn',
    'KafkaDsn',
    'NatsDsn',
    'MySQLDsn',
    'MariaDBDsn',
    'ClickHouseDsn',
    'SnowflakeDsn',
]


class PostgresDsn(_BaseMultiHostUrl):
    """A type that will accept any Postgres DSN.

    * User info required
    * TLD not required
    * Host required
    * Supports multiple hosts

    If further validation is required, these properties can be used by validators to enforce specific behaviour:

    ```python
    from pydantic import BaseModel, ValidationError, field_validator

    from pydantic_extra_types.dsn_types import PostgresDsn

    class MyDatabaseModel(BaseModel):
        db: PostgresDsn

        @field_validator('db')
        def check_db_name(cls, v):
            assert v.path and len(v.path) > 1, 'database must be provided'
            return v

    m = MyDatabaseModel(db='postgres://user:pass@localhost:5432/foobar')
    print(m.db)
    #> postgres://user:pass@localhost:5432/foobar
    ```
    """

    _constraints = UrlConstraints(
        host_required=True,
        allowed_schemes=[
            'postgres',
            'postgresql',
            'postgresql+asyncpg',
            'postgresql+pg8000',
            'postgresql+psycopg',
            'postgresql+psycopg2',
            'postgresql+psycopg2cffi',
            'postgresql+py-postgresql',
            'postgresql+pygresql',
        ],
    )

    @property
    def host(self) -> str:
        """The required URL host."""
        return self._url.host  # pyright: ignore[reportAttributeAccessIssue]


class CockroachDsn(AnyUrl):
    """A type that will accept any Cockroach DSN.

    * User info required
    * TLD not required
    * Host required
    """

    _constraints = UrlConstraints(
        host_required=True,
        allowed_schemes=[
            'cockroachdb',
            'cockroachdb+psycopg2',
            'cockroachdb+asyncpg',
        ],
    )

    @property
    def host(self) -> str:
        """The required URL host."""
        return self._url.host  # pyright: ignore[reportReturnType]


class AmqpDsn(AnyUrl):
    """A type that will accept any AMQP DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(allowed_schemes=['amqp', 'amqps'])


class RedisDsn(AnyUrl):
    """A type that will accept any Redis DSN.

    * User info required
    * TLD not required
    * Host required (e.g., `rediss://:pass@localhost`)
    """

    _constraints = UrlConstraints(
        allowed_schemes=['redis', 'rediss'],
        default_host='localhost',
        default_port=6379,
        default_path='/0',
        host_required=True,
    )

    @property
    def host(self) -> str:
        """The required URL host."""
        return self._url.host  # pyright: ignore[reportReturnType]


class MongoDsn(_BaseMultiHostUrl):
    """A type that will accept any MongoDB DSN.

    * User info not required
    * Database name not required
    * Port not required
    * User info may be passed without user part (e.g., `mongodb://mongodb0.example.com:27017`).
    """

    _constraints = UrlConstraints(allowed_schemes=['mongodb', 'mongodb+srv'], default_port=27017)


class KafkaDsn(AnyUrl):
    """A type that will accept any Kafka DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(allowed_schemes=['kafka'], default_host='localhost', default_port=9092)


class NatsDsn(_BaseMultiHostUrl):
    """A type that will accept any NATS DSN.

    NATS is a connective technology built for the ever increasingly hyper-connected world.
    It is a single technology that enables applications to securely communicate across
    any combination of cloud vendors, on-premise, edge, web and mobile, and devices.
    More: https://nats.io
    """

    _constraints = UrlConstraints(
        allowed_schemes=['nats', 'tls', 'ws', 'wss'], default_host='localhost', default_port=4222
    )


class MySQLDsn(AnyUrl):
    """A type that will accept any MySQL DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(
        allowed_schemes=[
            'mysql',
            'mysql+mysqlconnector',
            'mysql+aiomysql',
            'mysql+asyncmy',
            'mysql+mysqldb',
            'mysql+pymysql',
            'mysql+cymysql',
            'mysql+pyodbc',
        ],
        default_port=3306,
        host_required=True,
    )


class MariaDBDsn(AnyUrl):
    """A type that will accept any MariaDB DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(
        allowed_schemes=['mariadb', 'mariadb+mariadbconnector', 'mariadb+pymysql'],
        default_port=3306,
    )


class ClickHouseDsn(AnyUrl):
    """A type that will accept any ClickHouse DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(
        allowed_schemes=[
            'clickhouse+native',
            'clickhouse+asynch',
            'clickhouse+http',
            'clickhouse',
            'clickhouses',
            'clickhousedb',
        ],
        default_host='localhost',
        default_port=9000,
    )


class SnowflakeDsn(AnyUrl):
    """A type that will accept any Snowflake DSN.

    * User info required
    * TLD not required
    * Host required
    """

    _constraints = UrlConstraints(
        allowed_schemes=['snowflake'],
        host_required=True,
    )

    @property
    def host(self) -> str:
        """The required URL host."""
        return self._url.host  # pyright: ignore[reportReturnType]
