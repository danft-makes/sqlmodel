import sqlite3
from db import LOCALMODELSLIST,ALLMODELS

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
