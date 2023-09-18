import sqlite3
from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import _DEFAULT_TEMPLATE

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
llm = LlamaCpp(
    model_path="models/wizardcoder-python-34b-v1.0.Q4_K_M.gguf",
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

if __name__=='__main__':
    conn_query = sqlite3.connect('db/queries.db')
    c_query = conn_query.cursor()
    conn_analysis = sqlite3.connect('db/analysis.db')
    c_analysis = conn_analysis.cursor()
    c_query.execute('SELECT id, query FROM trio')
    queries = c_query.fetchall()
    for id, query in queries:
        QUERY = {'input': query}
        response = chain.run(QUERY)
        c_analysis.execute('UPDATE analysis SET response = ? WHERE id = ?', (response, id))
    conn_query.commit()
    conn_analysis.commit()
    conn_query.close()
    conn_analysis.close()
