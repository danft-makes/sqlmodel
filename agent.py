import os
import sqlite3
from langchain.llms import LlamaCpp, OpenAI
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from configs.prompts import _CLOSEINSTRUCTION_TEMPLATE, _ALPACA_TEMPLATE
from constants import *
from utils import ModelChooser, DatabaseManager
from db import ALLMODELS

class SQLQuery:
    def __init__(self, DATABASE_PATH):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def _syntax_checker(self, obj):
        # Dummy syntax checker
        return True

    def _classify_query(self, obj):
        # Dummy query classifier
        return "classification"

    def load_db(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables in the database:", self.cursor.fetchall())

    def get_response_columns(self):
        self.cursor.execute("PRAGMA table_info(analysis)")
        columns = [column[1] for column in self.cursor.fetchall() if 'response' in column[1]]
        return columns

    def process_responses(self):
        response_columns = self.get_response_columns()
        for column in response_columns:
            self.cursor.execute(f"SELECT {column} FROM analysis")
            responses = self.cursor.fetchall()
            for response in responses:
                syntax_check = self._syntax_checker(response)
                classification = self._classify_query(response)
                print(f"Syntax Check: {syntax_check}, Classification: {classification}")

class Agente:
    def __init__(self):
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def initialize_llm(self, MODEL_PATH):
        if MODEL_PATH == "gpt4":
            print("\nUsing OpenAI api key...\n")
            self.llm = OpenAI(temperature=0.0, verbose=True, streaming=True, callback_manager=self.callback_manager)
        else:
            self.llm = LlamaCpp(
                model_path=MODEL_PATH,
                callback_manager=self.callback_manager,
                verbose=True,
                temperature=0,
                max_tokens=750
            )
    
    def initialize_db(self):
        self.conn_query, self.c_query = DatabaseManager.connect_to_db('db/queries.db')
        self.conn_analysis, self.c_analysis = DatabaseManager.connect_to_db('db/analysis.db')
    
    def run_queries(self, chain,MODEL_TAG):
        queries = DatabaseManager.execute_query(self.c_query)
        if 'airoboros' in MODEL_TAG:
            for id, query in queries:
                QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
                response = chain.run(QUERY)
                DatabaseManager.update_analysis(self.c_analysis, id, response,MODEL_TAG)
        else:
            for id, query in queries:
                QUERY = {'input': query, 'instruction': instruction}
                response = chain.run(QUERY)
                DatabaseManager.update_analysis(self.c_analysis, id, response,MODEL_TAG)
        self.conn_query.commit()
        self.conn_analysis.commit()
        self.c_query.close()
        self.c_analysis.close()

    def main(self):
        # modified main made to run all local models
        ALLMODELS, ALLMODELSLIST = ModelChooser.choose_model()
        print(f'allmodels and allmodelslist are\n{ALLMODELS}\n{ALLMODELSLIST}')
        for i in range(len(ALLMODELS)):
            model = ALLMODELS[i]
            MODEL_TAG = ALLMODELSLIST[i]
            self.initialize_llm(model)
            if 'airoboros' in model:
                prompt = PromptTemplate(
                    input_variables=["input","text1","text2","metavars"], template=_CLOSEINSTRUCTION_TEMPLATE
                )
            else:
                prompt = PromptTemplate(
                    input_variables=["instruction","input"], template=_ALPACA_TEMPLATE
                )
            chain = LLMChain(llm=self.llm, prompt=prompt)
            self.initialize_db()
            self.run_queries(chain,MODEL_TAG.replace('-','').replace('.',''))


import sys

if __name__=='__main__':
    agent = Agente()
    agent.main()
    sql_query = SQLQuery('./db/analysis.db')
    sql_query.process_responses()
    sys.stdout = open('output.txt', 'w')
    sql_query.process_responses()
    sys.stdout.close()
