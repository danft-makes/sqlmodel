import sqlite3
from db.db import LOCALMODELSLIST,ALLMODELS

class SQLiteValidator: #TODO

    def __init__(self, db_path, column_name):
        self.db_path = db_path
        self.column_name = column_name

    def split_statements(self, contents):
        # Your regex implementation here
        pass

    def validate_column_entries(self):
        # Get all entries of the specified column
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT {self.column_name} FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]

            for table in tables:
                try:
                    # This will retrieve all unique entries in the column
                    cursor.execute(f"SELECT DISTINCT {self.column_name} FROM {table}")
                    entries = cursor.fetchall()

                    for entry in entries:
                        # Convert the entry tuple to a string
                        statement = str(entry[0])
                        # Validate the statement
                        self._validate_statement(statement)

                except sqlite3.OperationalError as e:
                    # This exception will catch issues like the column not existing in a table
                    print(f"Error with table {table}: {e}")

    def _validate_statement(self, statement):
        with sqlite3.connect(":memory:") as temp_db:
            try:
                temp_db.execute(statement)
            except Exception as e:
                print(f"Bad statement from column {self.column_name}. Ignoring.\n'{statement}'\nError: {e}")

class ModelChooser:
    @staticmethod
    def choose_model():
        CHOOSE_MODEL = input("model: ")
        if 'gpt' in CHOOSE_MODEL:
            print("Using GPT-4 model")
            return ALLMODELS["gpt4"]
        if "7" in CHOOSE_MODEL:
            return ALLMODELS["airoboros-7b-2.2-Q4"] 
        if "13" in CHOOSE_MODEL:
            return ALLMODELS["airoboros-13b-2.2-Q4"] 
        if CHOOSE_MODEL=="standard":
            return ALLMODELS["airoboros-13b-m2.0-Q5"]
        else: 
            LOCALMODELS = []
            for key in ALLMODELS.keys():
                LOCALMODELS.append(ALLMODELS[key])
            return [LOCALMODELS,LOCALMODELSLIST]

class DatabaseManager:
    @staticmethod
    def connect_to_db(db_name):
        conn = sqlite3.connect(db_name)
        return conn, conn.cursor()

    @staticmethod
    def execute_query(c_query):
        c_query.execute('SELECT id, query FROM trio')
        return c_query.fetchall()

    @staticmethod
    def update_analysis(c_analysis, id, response,MODEL_TAG=""):
        print(f'response is {response}\nMODEL_TAG is {MODEL_TAG}\n')
        c_analysis.execute('UPDATE analysis SET response'+MODEL_TAG+' = ? WHERE id = ?', (response, id))
