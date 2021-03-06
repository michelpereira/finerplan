import sqlite3

from flask import g


class SqliteDatabase(object):
    """Control a Sqlite Database bounded to a Flask application context."""
    def __init__(self, flaskapp=None):
        self._app = flaskapp
        if flaskapp is not None:
            self.init_app(flaskapp)

    def init_app(self, flaskapp):
        """Initializes the extension."""
        flaskapp.teardown_appcontext(self.teardown_db)
        self._app = flaskapp

    def connect(self):
        """Open a connection to the database storage."""
        if 'db' not in g:
            database = self._app.config['SQLITE_DATABASE']
            g.db = sqlite3.connect(database)
        return g.db

    def create_all(self):
        """Create the database tables from schema."""
        with self._app.open_resource('schema.sql', mode='r') as f:
            self.connect().executescript(f.read())

    @staticmethod
    def teardown_db(*args):
        """Close the database if it exists.

        Register this function as a Flask instance teardown_appcontext()
        handler to guarantee its execution, even if a before-request
        handler failed or was never executed.
        """
        _db = g.pop('db', None)
        if _db is not None:
            _db.close()

    def execute(self, *args, **kwargs):  # real signature unknown
        """Proxy to Sqlite Connection.execute()."""
        return self.connect().execute(*args, **kwargs)

    def commit(self):
        """Proxy to Sqlite Connection.commit()."""
        self.connect().commit()


db = SqliteDatabase()
