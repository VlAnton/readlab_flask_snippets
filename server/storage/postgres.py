from werkzeug import FileStorage

import psycopg2 as pg
import logging

from settings import settings


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
    
    def create_snippet(self, request: 'Request', **dict_args: dict) -> None:
        description: str = dict_args.get('description')
        code: str or 'FileStorage' = dict_args.get('code', request.files.get('code'))
        lang: str = dict_args.get('lang')

        if isinstance(code, FileStorage):
            with open(code.filename, 'r', encoding='utf-8') as f:
                code: str = f.read()

        QUERY = '''
            INSERT INTO snippets_table(description, lang, code)
            VALUES (%(description)s, %(lang)s, %(code)s);
        '''

        self._execute(
            QUERY,
            # url=url,
            description=description,
            lang=lang,
            code=code
        )

        logging.info('Successfully created')
    
    def _get_dict(self, snippet: 'Record') -> dict:
        print(type(snippet))
        result = {
            'snippet_id': snippet.snippet_id,
            'lang': snippet.lang,
            'description': snippet.description,
            'code': snippet.code
        }

        return result
    
    def _execute(self, query, **kwargs) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, kwargs)

        self.connection.commit()

    def _fetch(self, query, **kwargs):
        with self.connection.cursor(cursor_factory=pg.extras.NamedTupleCursor) as cursor:
            cursor.execute(query, kwargs)
            fetched = cursor.fetchall()

            return fetched

postgres = PostgresClient(
    settings.PG_HOST,
    settings.PG_PORT,
    settings.PG_DBNAME,
    settings.PG_USER, settings.PG_PASS
)