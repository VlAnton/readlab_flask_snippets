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
            SELECT * FROM snippets_table;
        '''
        snippets = self._fetch(QUERY)
        snippets_str = '\n'.join(map(str, snippets))
        logging.info(f'Fetched {len(snippets)} issues:\n{snippets_str}')

        return [
            self._get_dict(snippet)
            for snippet in snippets
        ]

    def retrieve_snippet(self, snippet_uid: str) -> dict:
        QUERY = '''
            SELECT description, snippet_uid, created_at
            FROM snippets_table
            
            WHERE snippets_table.snippet_uid = %(snippet_uid)s;
        '''
        response: list = self._fetch(
            QUERY,
            snippet_uid=snippet_uid
        )
        if not response:
            return {}

        snippet: dict = response.pop()

        logging.info(f'Fetched {len(snippet)} issues:\n{str(snippet)}')

        return self._get_dict(snippet)
    
    def create_snippet(self, request: 'Request', **dict_args: dict):
        # TODO: сделать список файлов и поменять базу так, чтобы был foreignKey на таблицу files
        # В ней будет хранится список файлов и имена
        files_dict = dict()
        snippet_uid = str(uuid4())

        description: str = dict_args.get('description')
        # files: str = dict_args.get('files')
        # lang: str = dict_args.get('lang')

        # files_list.append(files)

        for file in request.files.getlist('files'):
            filename: str = file.filename
            ext: str = filename.split('.').pop()

            lang: str = self.ALLOWED_LANGUAGES.get(ext)

            if lang:
                with open(filename, 'r', encoding='utf-8') as f:
                    file: str = f.read()

                files_dict[lang] = file
        
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
        print('asdasdfsadf', snippet)
        result = {
            'snippet_uid': snippet.snippet_uid,
            'description': snippet.description,
            'created_at': snippet.created_at
        }

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