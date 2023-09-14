from langchain.llms import LlamaCpp
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

table_info="""
branch_text = (
    "Esta tabela detalha as filiais da empresa: ID da filial, nome do gerente, cidade e nome específico. "
    "Consulte usando 'branch_id', 'manager_name', 'city' e 'branch_name'."
)

customer_text = (
    "Esta tabela lista detalhes do cliente: ID, idade, data de criação, pontuação RFM, nome, cidade, telefone e data da última compra. "
    "Consulte usando 'customer_id', 'name' ou 'phone'."
)

inventory_text = (
    "Esta tabela rastreia o inventário de produtos nas filiais, notando ID do inventário, ID do produto, ID da filial e quantidade. "
    "Está vinculada às tabelas de produto e filial. Consulte usando 'product_id' ou 'branch_id'."
)

product_text = (
    "Esta tabela armazena dados do produto: ID do produto, nome, categoria (por exemplo, Eletrônicos), data de adição e descrição. "
    "Consulte com 'product_id', 'category' ou 'name'."
)

sales_text = (
    "Esta tabela registra transações de vendas, detalhando ID de venda, data, ID do cliente, ID da filial, ID do produto, quantidade e preço total. "
    "Ela se vincula às tabelas de cliente, filial e produto. Consulte com 'sale_id', 'customer_id' ou 'product_id'."
)"""

_DEFAULT_TEMPLATE="""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct sqlite query to run, don't return anything else besides the query.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
If the question does not seem related to the database, just return "I don't know" as the answer.

Question: {input}

Table: {table_info}

### Response: 
"""

db = SQLDatabase.from_uri("sqlite:///dmp.db")  # Load the SQLite database
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
    input_variables=["input", "table_info"], template=_DEFAULT_TEMPLATE
)
chain = LLMChain(llm=llm, prompt=prompt)

if __name__=='__main__':
    QUERY = input("QUERY = ")
    QUERY = {'input':QUERY,'table_info':table_info}
    # Load db and Llama
    print(chain.run(QUERY))
