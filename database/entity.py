from urllib.parse import urlparse
from peewee import *

from config import get_database_url

db = SqliteDatabase(get_database_url())

@staticmethod
def get_database():
    return db

class BaseModel(Model):
    class Meta:
        database = db

class CefrLevel(BaseModel):
    id = PrimaryKeyField()
    level = CharField()

    class Meta:
        table_name = 'cefr_level'

class Type(BaseModel):
    id = PrimaryKeyField()
    type = CharField()

    class Meta:
        table_name = 'type'

class Word(BaseModel):
    id = PrimaryKeyField()
    word = CharField()
    type_id = ForeignKeyField(Type, backref='words')
    level_id = ForeignKeyField(CefrLevel, backref='words')
    pos = CharField()
    definition_url = CharField()
    voice_url = CharField()

    class Meta:
        table_name = 'word'
    
    def get_word_from_url(self):
        parsed_url = urlparse(self.definition_url)
        path = parsed_url.path
        parts = path.split('/')
        return parts[-1]

class Definition(BaseModel):
    id = PrimaryKeyField()
    definition = TextField()
    img_url = CharField()
    word_id = ForeignKeyField(Word, backref='definitions')

    class Meta:
        table_name = 'definition'

class SentenceDefinition(BaseModel):
    id = PrimaryKeyField()
    sentence = TextField()
    definition_id = ForeignKeyField(Definition, backref='sentence_definitions')

    class Meta:
        table_name = 'sentence_definition'
