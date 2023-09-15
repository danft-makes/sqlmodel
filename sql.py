from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from prompts import _DEFAULT_TEMPLATE

db = SQLDatabase.from_uri("sqlite:///db/analysis_db.db")  # Load the SQLite database
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
llm = LlamaCpp(
    model_path="models/wizard.gguf",
    callback_manager=callback_manager,
    verbose=False,
    max_tokens=500,
    n_ctx=4000,
    n_batch=256,
    temperature=0,
)  # Initialize the LlamaCpp model

prompt = PromptTemplate(
    input_variables=["input"], template=_DEFAULT_TEMPLATE
)
chain = LLMChain(llm=llm, prompt=prompt)

# manual query db

import sqlite3

if __name__=='__main__':
    conn = sqlite3.connect('db/query.db')
    c = conn.cursor()
    c.execute('SELECT query FROM trio')
    queries = c.fetchall()
    for query in queries:
        QUERY = {'input': query[0]}
        response = chain.run(QUERY)
    conn.close()
