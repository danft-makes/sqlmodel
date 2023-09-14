from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import create_sql_agent, AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
If the question does not seem related to the database, just return "I don't know" as the answer.
Question: {input}
Table: {table}
### Response: I should look at the tables in the database to see what I can query. Then I should query the schema of the most relevant tables.
{agent_scratchpad}
"""

if __name__=='__main__':
    QUERY = input("QUERY = ")
    # Load db and Llama
    db = SQLDatabase.from_uri("sqlite:///dmp.db")  # Load the SQLite database
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    llm = LlamaCpp(
        model_path="models/wizard.gguf",
        #callback_manager=callback_manager,
        verbose=False,
        max_tokens=500,
        n_ctx=4000,
        n_batch=256,
        temperature=0,
    )  # Initialize the LlamaCpp model

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prefix=SQL_PREFIX,
        suffix=SQL_SUFFIX
    )

    response = agent_executor.run(QUERY)  # Run the query using the database chain
    print(response)  # Print the response
    MAX_RETRIES = 5  # Set the maximum number of retries
    for attempt in range(MAX_RETRIES):
        try:
            agent_response = agent_chain.run(QUERY)

        except ValueError as e:
            response = str(e)

            if not response.startswith("Could not parse LLM output: `"):
                raise e

            response = response.removeprefix("Could not parse LLM output: `").removesuffix(
                "`"
            )

            print(f"feeding back {QUERY}")
            QUERY = response  # Feed the response back into the agent

        # If we've reached the maximum number of retries, give up
        if attempt == MAX_RETRIES - 1:
            print("Error: Agent failed to run after multiple attempts")
