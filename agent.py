import os
import sqlite3
from langchain.llms import LlamaCpp, OpenAI
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import _CLOSEINSTRUCTION_TEMPLATE
from constants import *
from utils import ModelChooser, DatabaseManager


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
    
    def run_queries(self, chain):
        queries = DatabaseManager.execute_query(self.c_query)
        for id, query in queries:
            QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
            response = chain.run(QUERY)
            DatabaseManager.update_analysis(self.c_analysis, id, response)
        self.conn_query.commit()
        self.conn_analysis.commit()
        self.c_query.close()
        self.c_analysis.close()

    def main(self):
        MODEL_PATH = ModelChooser.choose_model()
        self.initialize_llm(MODEL_PATH)
        prompt = PromptTemplate(
            input_variables=["input","text1","text2","metavars"], template=_CLOSEINSTRUCTION_TEMPLATE
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        self.initialize_db()
        self.run_queries(chain)


if __name__=='__main__':
    agent = Agente()
    agent.main()