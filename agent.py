import os
import sqlite3
from langchain.llms import LlamaCpp, OpenAI
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from configs.prompts import _XWIN_TEMPLATE
from constants import *
from utils import ModelChooser, DatabaseManager
from db import ALLMODELS

class Agente:
    def __init__(self):
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    def initialize_llm(self, MODEL_PATH):
        self.llm = LlamaCpp(
            model_path=MODEL_PATH,
            callback_manager=self.callback_manager,
            verbose=True,
            temperature=0,
            max_tokens=1500
        )

    def initialize_db(self):
        self.conn_query, self.c_query = DatabaseManager.connect_to_db('db/queries.db')
        self.conn_analysis, self.c_analysis = DatabaseManager.connect_to_db('db/analysis.db')

    def run_queries(self, chain,MODEL_TAG):
        queries = DatabaseManager.execute_query(self.c_query)
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
        for i in range(len(ALLMODELS)):
            prompt = PromptTemplate(
                input_variables=["instruction","input"], template=_XWIN_TEMPLATE
            )
            chain = LLMChain(llm=self.llm, prompt=prompt)
            self.initialize_db()
            self.run_queries(chain,MODEL_TAG.replace('-','').replace('.',''))


if __name__=='__main__':
    agent = Agente()
    agent.main()
