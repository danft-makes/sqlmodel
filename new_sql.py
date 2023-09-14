# This file is a refactored version of sql.py where the code has been encapsulated into a class named SQLAgent.

from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate

# The SQLAgent class encapsulates the initialization and usage of the llm, callback, database, prompt, and agent.
class SQLAgent:
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

    def __init__(self):
        self.db = SQLDatabase.from_uri("sqlite:///dmp.db")  # Load the SQLite database
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
        self.llm = LlamaCpp(
            model_path="models/wizard.gguf",
            #callback_manager=self.callback_manager,
            verbose=False,
            max_tokens=500,
            n_ctx=4000,
            n_batch=256,
            temperature=0,
        )  # Initialize the LlamaCpp model

        self.PROMPT = PromptTemplate(
            input_variables=["input", "table_info", "dialect"], template=self._DEFAULT_TEMPLATE
        )

        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True, use_query_checker=True, return_intermediate_steps=False, return_direct=True, agent_type=AgentType.OPENAI_FUNCTIONS)

    # The run_query method takes a query as input and returns the result of the query.
    def run_query(self, query):
        response = self.db_chain.run(query)  # Run the query using the database chain
        return response

if __name__=='__main__':
    # The main script creates an instance of SQLAgent and uses it to run queries in a loop.
    agent = SQLAgent()
    while True:
        QUERY = input("Coloque QUERY: ")  # Get the query from the user
        response = agent.run_query(QUERY)
        print(response)  # Print the response
