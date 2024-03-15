import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('C:\\Users\\Kolar\\IdeaProjects\\oxford-word-list\\database\\my_database.db')
        self.cursor = self.conn.cursor()
        
    def initialize(self):
        db = DatabaseManager()
        db.create_table(
        f'''CREATE TABLE IF NOT EXISTS CEFR_LEVEL (
            ID INTEGER PRIMARY KEY,
            LEVEL TEXT
        );''')
        self.__initialize_cerf_data()
        
        db.create_table(
        f'''CREATE TABLE IF NOT EXISTS TYPE (
            ID INTEGER PRIMARY KEY,
            TYPE TEXT
        );''')
        self.__initialize_type_data()
                
        db.create_table(
        f'''CREATE TABLE IF NOT EXISTS SENTENCE_DEFINITION (
            ID INTEGER PRIMARY KEY,
            SENTENCE TEXT,
            DEFINITION_ID INTEGER,
            FOREIGN KEY (DEFINITION_ID) REFERENCES DEFINITION(ID)
        );''')

        db.create_table(
        f'''CREATE TABLE IF NOT EXISTS DEFINITION (
            ID INTEGER PRIMARY KEY,
            DEFINITION TEXT,
            WORD_ID INTEGER,
            FOREIGN KEY (WORD_ID) REFERENCES WORD(ID)
        );''')

        db.create_table(
        f'''CREATE TABLE IF NOT EXISTS WORD (
            ID INTEGER PRIMARY KEY,
            WORD TEXT,
            TYPE_ID INTEGER,
            LEVEL_ID INTEGER,
            POS TEXT,
            DEFINITION_URL TEXT,
            VOICE_URL TEXT,
            FOREIGN KEY (LEVEL_ID) REFERENCES CEFR_LEVEL(ID)
            FOREIGN KEY (TYPE_ID) REFERENCES TYPE(ID)
        );''')


    def create_table(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_into_table(self, table_name, data):
        placeholders = ', '.join('?' * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', values)
        self.conn.commit()
        
    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        
    def __initialize_cerf_data(self):
        self.insert_into_table("CEFR_LEVEL", {"ID": 1, "LEVEL": "A1"})
        self.insert_into_table("CEFR_LEVEL", {"ID": 2, "LEVEL": "A2"})
        self.insert_into_table("CEFR_LEVEL", {"ID": 3, "LEVEL": "B1"})
        self.insert_into_table("CEFR_LEVEL", {"ID": 4, "LEVEL": "B1"})
        self.insert_into_table("CEFR_LEVEL", {"ID": 5, "LEVEL": "C1"})        
        
    def __initialize_type_data(self):
        self.insert_into_table("TYPE", {"ID": 1, "TYPE": "Oxford 3000"})
        self.insert_into_table("TYPE", {"ID": 2, "TYPE": "Oxford 5000"})
        
        
# db = DatabaseManager()
# db.initialize()
# db.close()