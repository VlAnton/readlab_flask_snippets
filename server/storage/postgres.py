from psycopg2.extras import NamedTupleCursor
from settings import settings

import psycopg2 as pg
import logging
import json


class PostgresClient:
    def __init__(self, host, port, dbname, user, password):
        self.connection = pg.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password,
            target_session_attrs='read-write'
        )

    def get_snippets(self):
        QUERY = '''
            SELECT * FROM snippets_table;
        '''
        snippets = self._fetch(QUERY)
        snippets_str = '\n'.join(map(str, snippets))
        logging.info(f'Fetched {len(snippets)} issues:\n{snippets_str}')

        snippets_dict = [
            self._get_dict(snippet)
            for snippet in snippets
        ]

        return snippets_dict
    
    def create_snippet(self, code: str, description: str, url: str):
        QUERY = '''
            INSERT INTO snippets_table(code, description, url)
            VALUES (%(code)s, %(description)s, %(url)s);
        '''
        self._execute(
            QUERY,
            code=code,
            description=description,
            url=url
        )

        logging.info('Successfully created')

    
    def _get_dict(self, snippet):
        print(snippet)
        return {
            'snippet_id': snippet.snippet_id,
            'code': snippet.code,
            'description': snippet.description,
            'url': snippet.url
        }
    
    def _execute(self, query, **kwargs) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, kwargs)

        self.connection.commit()

    def _fetch(self, query, **kwargs):
        with self.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, kwargs)

            fetched = cursor.fetchall()

            return fetched

postgres = PostgresClient(
    settings.PG_HOST,
    settings.PG_PORT,
    settings.PG_DBNAME,
    settings.PG_USER, settings.PG_PASS
)