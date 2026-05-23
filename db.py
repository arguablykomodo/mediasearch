from os import path
from peewee import DateTimeField, Model, SqliteDatabase, TextField
from playhouse.sqlite_ext import FTS5Model, RowIDField, SearchField

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = db

class File(BaseModel):
    path: TextField = TextField(unique=True, null=False)
    text: TextField = TextField(null=True)
    audio: TextField = TextField(null=True)
    mtime: DateTimeField = DateTimeField(null=False)

class FileIndex(FTS5Model):
    path: SearchField = SearchField()
    text: SearchField = SearchField()
    audio: SearchField = SearchField()

    class Meta:
        database = db
        options = {
            "content": File,
            "content_rowid": File.id,
        }

def connect(directory: str):
    db_path = path.realpath(path.join(directory, ".mediasearch.sqlite"))
    db.init(db_path)
    db.connect()
    db.create_tables([File, FileIndex])
