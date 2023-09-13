from llama_index import SQLDatabase
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
)
engine = create_engine('sqlite:///dmp.db')
ALL_TABLES =["branch","customer","inventory","product","sales"]
sql_database = SQLDatabase(engine, include_tables = ALL_TABLES)
print(sql_database.table_info)
from llama_index.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine, NLSQLTableQueryEngine
from llama_index.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index import VectorStoreIndex
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Load llama cpp
from llama_index import LLMPredictor, ServiceContext
from langchain.llms import LlamaCpp
llama = LlamaCpp(
    model_path="/home/magus/projects/text-generation-webui/models/TheBloke_WizardCoder-Python-34B-V1.0-GGUF-sus/wizardcoder-python-34b-v1.0.Q4_K_M.gguf",
    temperature=0,
    callback_manager=callback_manager,
    verbose=False,
    max_tokens=500,
    n_ctx=4000,
    n_batch=256,
)
llm_predictor = LLMPredictor(llm=llama)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
query_engine = NLSQLTableQueryEngine(sql_database, tables=ALL_TABLES, service_context=service_context)
if __name__=='__main__':
    while True:
        QUERY = input('Coloque QUERY: ')
        response = query_engine.query(QUERY)
        print(response,response.metadata["result"])

