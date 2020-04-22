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
    def from_env(cls, path) -> 'Settings':
        load_dotenv(dotenv_path=path)
        variables = {name: cls._field_types[name](getenv(name)) for name in cls._fields}
        return cls(**variables)


script_path = path.dirname(path.abspath(__file__))
settings = Settings.from_env(f'{script_path}/.env')
