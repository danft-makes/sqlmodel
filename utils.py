import sqlite3
from db import LOCALMODELSLIST,ALLMODELS

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


class SQLQuery:
    def __init__(self, query):
        self.query = query
        self.is_valid = is_valid_syntax(query)
        self.query_classification = self._classify_query() if not self.is_valid else None

    def _classify_query(self):
        # Classify the query if it's not valid
        return query_type(self.query)

    @classmethod
    def from_db(cls, db_path):
        # Load SQL queries from a .db file and instantiate multiple SQLQuery objects
        queries = load_queries_from_db(db_path)
        return [cls(query) for query in queries]

# Example hypothetical functions:
def is_valid_syntax(query): #TODO
    # Check if the SQL query has valid syntax
    return True if "SELECT" in query else False

def query_type(query): #TODO
    # Classify the type of error in the query
    if "SELECT" not in query:
        return "incomplete query"
    return "unknown error"

def load_queries_from_db(db_path):
    # Load SQL queries from a .db file
    return ["SELECT * FROM users", "SELECT name FROM", "DELETE FROM users WHERE id=1; SELECT"]

# To use the SQLQuery class to analyze a .db file:
if __name__ == "__main__":
    queries = SQLQuery.from_db("path_to_db_file.db")
    for query_obj in queries:
        if not query_obj.is_valid:
            print(f"Query: {query_obj.query}")
            print(f"Classification: {query_obj.query_classification}")

