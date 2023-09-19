import sqlite3
from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import _DEFAULT_TEMPLATE
from constants import *

if __name__=='__main__':
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    CHOOSE_MODEL = input("7b or 13b?")
    if "7" in CHOOSE_MODEL:
        MODEL_PATH = "/home/shared/airoboros-l2-7b-2.2.Q4_K_M.gguf"
    else:
        MODEL_PATH = "/home/shared/airoboros-l2-13b-2.2.Q4_K_M.gguf"
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

    conn_query = sqlite3.connect('db/queries.db')
    c_query = conn_query.cursor()
    conn_analysis = sqlite3.connect('db/analysis.db')
    c_analysis = conn_analysis.cursor()
    c_query.execute('SELECT id, query FROM trio')
    queries = c_query.fetchall()
    for id, query in queries:
        QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
        response = chain.run(QUERY)
        c_analysis.execute('UPDATE analysis SET response = ? WHERE id = ?', (response, id))
    conn_query.commit()
    conn_analysis.commit()
    conn_query.close()
    conn_analysis.close()
