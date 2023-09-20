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

def initialize_llm(MODEL_PATH):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    if MODEL_PATH=="gpt4":
        print("\nUsing OpenAI api key...\n")
        llm = OpenAI(temperature=0.0)
    elif isinstance(MODEL_PATH,list):
        # run the main for every model in the list MODEL_PATH
    else:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            callback_manager=callback_manager,
            verbose=True,
            temperature=0,
            max_tokens=750
        )
    return llm

def initialize_db():
    conn_query, c_query = DatabaseManager.connect_to_db('db/queries.db')
    conn_analysis, c_analysis = DatabaseManager.connect_to_db('db/analysis.db')
    return conn_query, c_query, conn_analysis, c_analysis

def run_queries(chain, c_query, c_analysis):
    queries = DatabaseManager.execute_query(c_query)
    for id, query in queries:
        QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
        response = chain.run(QUERY)
        DatabaseManager.update_analysis(c_analysis, id, response)
    conn_query.commit()
    conn_analysis.commit()
    c_query.close()
    c_analysis.close()

def main():
    MODEL_PATH = ModelChooser.choose_model()
    llm = initialize_llm(MODEL_PATH)
    prompt = PromptTemplate(
            input_variables=["input","text1","text2","metavars"], template=_CLOSEINSTRUCTION_TEMPLATE # vars in string format 'key0:value0\nkey1:value1\n...\nkeyn:valuen
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    conn_query, c_query, conn_analysis, c_analysis = initialize_db()
    run_queries(chain, c_query, c_analysis)

if __name__=='__main__':
    main()
