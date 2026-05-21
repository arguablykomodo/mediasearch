from os import path
from peewee import Model, SqliteDatabase, TextField

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = db

class File(BaseModel):
    path: TextField = TextField(unique=True)
    text: TextField = TextField(null=True)
    audio: TextField = TextField(null=True)

def connect(directory: str):
    db_path = path.realpath(path.join(directory, ".mediasearch.sqlite"))
    db.init(db_path)
    db.connect()
    db.create_tables([File])
