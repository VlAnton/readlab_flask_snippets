from psycopg2.extras import NamedTupleCursor
from psycopg2 import errors

from uuid import uuid4

import psycopg2 as pg
import logging

from settings import settings


class PostgresClient:
    ALLOWED_LANGUAGES = {
        'py': 'python',
        'js': 'javascript',
        'html': 'html'
    }

    def __init__(self, host, port, dbname, user, password):
        self.connection = pg.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password,
            target_session_attrs='read-write'
        )

    def get_snippets(self) -> list:
        QUERY = """
            SELECT
                snippet_uid,
                created_at,
                public,
                description
            FROM snippets_table;
        """
        snippets: list = self._fetch(QUERY)
        logging.info(f'Fetched {len(snippets)} snippets')

        return snippets

    def retrieve_snippet(self, snippet_uid):
        QUERY = """
            SELECT
                created_at,
                public,
                description
            FROM snippets_table
            WHERE snippet_uid = '%s';
        """ % snippet_uid
        response: list = self._fetch(
            QUERY,
            snippet_uid=snippet_uid
        )
        logging.info(f'Fetched snippet: {str(response)}')

        return response
    
    def create_snippet(self, request: 'Request', **dict_args: dict):
        snippet_uid = str(uuid4())
        description: str = dict_args.get('description')
        QUERY = """
            INSERT INTO snippets_table(description, snippet_uid)
            VALUES (%(description)s, %(snippet_uid)s);
        """

        self._execute(
            QUERY,
            description=description,
            snippet_uid=snippet_uid
        )
        logging.info('Snippet is created')
    
    def _execute(self, query, **kwargs) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, kwargs)

        self.connection.commit()

    def _fetch(self, query, **kwargs):
        with self.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            fetched = []
            try:
                cursor.execute(query, kwargs)
            except Exception as ex:
                logging.error(f'Fetched unsuccessfully with query={query} and error: {str(ex)}')
            else:
                fetched = cursor.fetchall()

            return fetched

postgres = PostgresClient(
    settings.PG_HOST,
    settings.PG_PORT,
    settings.PG_DBNAME,
    settings.PG_USER,
    settings.PG_PASS
)
