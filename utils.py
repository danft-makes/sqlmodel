import sqlite3
from db import LOCALMODELSLIST,ALLMODELS

class ModelChooser:
    @staticmethod
    def choose_model():
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
