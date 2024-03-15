from peewee import *

db = SqliteDatabase('C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\database\\my_database.db')

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
