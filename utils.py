import sqlite3

class ModelChooser:
    ALLMODELS = {'gpt4':'gpt4','airoboros-7b-2.2-Q4':'/home/shared/models/airoboros-l2-7b-2.2.Q4_K_M.gguf','airoboros-13b-2.2-Q4':'/home/shared/models/airoboros-l2-13b-2.2.Q4_K_M.gguf','airoboros-13b-m2.0-Q5':'/home/shared/models/airoboros-l2-13b-gpt4-m2.0.Q5_K_M.gguf'}

    @staticmethod
    def choose_model():
        CHOOSE_MODEL = input("model: ")
        if 'gpt' in CHOOSE_MODEL:
            print("Using GPT-4 model")
            return ModelChooser.ALLMODELS["gpt4"]
        if "7" in CHOOSE_MODEL:
            return ModelChooser.ALLMODELS["airoboros-7b-2.2-Q4"] 
        if "13" in CHOOSE_MODEL:
            return ModelChooser.ALLMODELS["airoboros-13b-2.2-Q4"] 
        if CHOOSE_MODEL=="ALL":
            LOCALMODELS = []
            for key in CHOOSE_MODEL.keys():
                if key=='gpt4':
                    continue
                LOCALMODELS.append(CHOOSE_MODEL[key])
            return LOCALMODELS 
        else: 
            return ModelChooser.ALLMODELS["airoboros-13b-m2.0-Q5"]

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
    def update_analysis(c_analysis, id, response):
        c_analysis.execute('UPDATE analysis SET response = ? WHERE id = ?', (response, id))
