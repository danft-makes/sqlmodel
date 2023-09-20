import os
import sqlite3
from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import _DEFAULT_TEMPLATE
from constants import *
from openai import OpenAI

def choose_model():
    USE_GPT4 = os.getenv('USE_GPT4', 'False').lower() in ['true', '1', 't', 'y', 'yes']
    if USE_GPT4:
        print("Using GPT-4 model")
        return "/path/to/gpt4/model"
    else:
        CHOOSE_MODEL = input("7b or 13b?")
        if "7" in CHOOSE_MODEL:
            return "/home/shared/airoboros-l2-7b-2.2.Q4_K_M.gguf"
        else:
            return "/home/shared/airoboros-l2-13b-2.2.Q4_K_M.gguf"

def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn.cursor()

def execute_query(c_query):
    c_query.execute('SELECT id, query FROM trio')
    return c_query.fetchall()

def update_analysis(c_analysis, id, response):
    c_analysis.execute('UPDATE analysis SET response = ? WHERE id = ?', (response, id))

if __name__=='__main__':
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    MODEL_PATH = choose_model()
    if 'gpt' in MODEL_PATH:
        llm = OpenAI(temperature=0.0)
    else:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            callback_manager=callback_manager,
            verbose=True,
            temperature=0,
        )

    prompt = PromptTemplate(
            input_variables=["input","text1","text2","metavars"], template=_DEFAULT_TEMPLATE # vars in string format 'key0:value0\nkey1:value1\n...\nkeyn:valuen
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    c_query = connect_to_db('db/queries.db')
    c_analysis = connect_to_db('db/analysis.db')
    queries = execute_query(c_query)
    for id, query in queries:
        QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
        response = chain.run(QUERY)
        update_analysis(c_analysis, id, response)
    conn_query.commit()
    conn_analysis.commit()
    conn_query.close()
    conn_analysis.close()
