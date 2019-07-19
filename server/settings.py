from typing import NamedTuple

from os import getenv, path

from dotenv import load_dotenv


class Settings(NamedTuple):
    PG_HOST: str
    PG_PORT: int
    PG_DBNAME: str
    PG_USER: str
    PG_PASS: str

    @classmethod
    def from_env(cls) -> 'Settings':
        variables = {name: cls._field_types[name](getenv(name)) for name in cls._fields}

        return cls(**variables)

    @classmethod
    def from_dotenv(cls, *paths: str) -> 'Settings':
        for path in paths:
            load_dotenv(dotenv_path=path)

        return cls.from_env()


script_path = path.dirname(path.abspath(__file__))
env = getenv('PYTHON_ENV', default='development')

settings = Settings.from_dotenv(
    f'{script_path}/.env',
    f'{script_path}/.env.{env}'
)