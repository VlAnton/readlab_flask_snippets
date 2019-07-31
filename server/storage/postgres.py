from werkzeug import FileStorage, ImmutableMultiDict

from psycopg2.extras import NamedTupleCursor

from uuid import uuid4

import psycopg2 as pg
import logging

from settings import settings


class PostgresClient:
    ALLOWED_LANGUAGES = {
        'py': 'python',
        'js': 'javascript',
        'php': 'php',
        'c': 'C',
        'html': 'html'
    }

    def __init__(self, host, port, dbname, user, password):
        self.connection = pg.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password,
            target_session_attrs='read-write'
        )

    def get_snippets(self) -> list:
        QUERY = '''
            SELECT
                s.snippet_uid,
                s.created_at,
                s.public,
                s.description,
                COUNT(f) AS files_count
            FROM snippets_table AS s
            INNER JOIN file AS f
            ON f.snippet_uid = s.snippet_uid GROUP BY s.snippet_uid;
        '''
        snippets: list = self._fetch(QUERY)

        snippets_str: str = '\n'.join(map(str, snippets))
        logging.info(f'Fetched {len(snippets)} snippets:\n{snippets_str}')

        return [
            self._get_dict(snippet)
            for snippet in snippets
        ]

    def retrieve_snippet(self, snippet_uid: str) -> dict:
        QUERY = '''
            SELECT
                s.description,
                s.snippet_uid,
                s.created_at,
                s.public,
                file.content,
                file.lang,
                file.file_id
            FROM snippets_table AS s
            INNER JOIN file ON s.snippet_uid = file.snippet_uid
            WHERE s.snippet_uid = %(snippet_uid)s;
        '''
        response: list = self._fetch(
            QUERY,
            snippet_uid=snippet_uid
        )
        if not response:
            return {}

        snippet: dict = self._get_dict(response[0])
        snippet['files'] = []

        for item in response:
            snippet['files'].append({
                'file_id': item.file_id,
                'lang': item.lang,
                'content': item.content
            })

        logging.info(f'Fetched snippet with {len(response)} files:\n{str(snippet)}')

        return snippet
    
    def create_snippet(self, request: 'Request', **dict_args: dict):
        snippet_uid = str(uuid4())
        description: str = dict_args.get('description')

        files_dict = dict()
        files_list: list = dict_args.get('files')

        if not files_list:
            raise ValueError('no files given')

        for file in files_list:
            ext: str = file.filename.split('.').pop()
            lang: str = self.ALLOWED_LANGUAGES.get(ext)

            if lang:
                file: bytes = file.read()

                files_dict[lang] = file.decode('utf-8')

        if not files_dict:
            raise ValueError('all files are in incorrect format or else')
        
        try:
            QUERY = '''
                INSERT INTO snippets_table(description, snippet_uid)
                VALUES (%(description)s, %(snippet_uid)s);
            '''

            self._execute(
                QUERY,
                description=description,
                snippet_uid=snippet_uid
            )
            self._handle_files(files_dict, snippet_uid)

            logging.info('Snippet is created')

        except BaseException as err:
            raise ValueError(str(err))

    def _handle_files(self, files_dict: dict, snippet_uid: str):
        for lang, content in files_dict.items():
            QUERY = '''
                INSERT INTO file(content, lang, snippet_uid)
                VALUES(%(content)s, %(lang)s, %(snippet_uid)s);
            '''

            self._execute(
                QUERY,
                content=content,
                lang=lang,
                snippet_uid=snippet_uid
            )

        logging.info('Files are handled')

    
    def _get_dict(self, snippet: 'Record') -> dict:
        result = {
            'snippet_uid': snippet.snippet_uid,
            'description': snippet.description,
            'created_at': snippet.created_at,
            'public': snippet.public
        }

        if hasattr(snippet, 'files_count'):
            result['files_count'] = snippet.files_count

        return result
    
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