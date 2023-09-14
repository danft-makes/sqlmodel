from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate


_DEFAULT_TEMPLATE = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then return only the query without snippets.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query.
{table_info}"""

# Load db and Llama
db = SQLDatabase.from_uri("sqlite:///dmp.db")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path="models/wizard.gguf",
    #callback_manager=callback_manager,
    verbose=False,
    max_tokens=500,
    n_ctx=4000,
    n_batch=256,
    temperature=0,
)

PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, use_query_checker=True, return_intermediate_steps=False, return_direct=True, agent_type=AgentType.OPENAI_FUNCTIONS)

if __name__=='__main__':
    while True:
        QUERY = input("Coloque QUERY: ")
        response = db_chain.run(QUERY)
        print(response)
