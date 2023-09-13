from llama_index import SQLDatabase, VectorStoreIndex, LLMPredictor, ServiceContext, set_global_service_context
from llama_index.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from llama_index.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from sqlalchemy import create_engine
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load db
engine = create_engine('sqlite:///dmp.db')
sql_database = SQLDatabase(engine)

# Load llama.cpp
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llama = LlamaCpp(
    model_path="models/wizard.gguf",
    callback_manager=callback_manager,
    verbose=False,
    max_tokens=500,
    n_ctx=4000,
    n_batch=256,
    temperature=0,
)
print(f"Loaded model: {llama}. Updating service_context...")
service_context = ServiceContext.from_defaults(llm=llama)
set_global_service_context(service_context)
print(f"Done")

# Make index
table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = []
all_table_names = ["branch","customer","inventory","product","sales"]
for table_name in all_table_names:
    table_schema_objs.append(SQLTableSchema(table_name=table_name))
    print(f"Appending table {table_name} ")
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex
)

# Make query engine
query_engine = SQLTableRetrieverQueryEngine(
    sql_database,
    obj_index.as_retriever(similarity_top_k=1),
    service_context=service_context
)

if __name__=='__main__':
    while True:
        QUERY = input('Coloque QUERY: ')
        response = query_engine.query(QUERY)
        print(response)
