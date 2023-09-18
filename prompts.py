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
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
If the question does not seem related to the database, just return "I don't know" as the answer.

The tables you can query are:
Table inventory has columns = [inventory_id,product_id,branch_id,quantity]
Table sales has columns = [sale_id,sale_date,customer_id,branch_id,product_id,quantity,total_price]
Table customer has columns = [customer_id,creation_date,rfm_class,name,city,phone,last_purchase_date]
Table branch has columns = [branch_id,manager_id,city]
Table product has columns = [product_id,name,category,creation_date,description]
JOINS ARE = [sales.customer_id = customer.customer_id, sales.branch_id = branch.branch_id, sales.product_id = product.product_id, inventory.product_id = product.product_id, inventory.branch_id = branch.branch_id, branch.manager_id = manager.manager_id]

rfm_class can be four values: 'Precisam de atenção', 'Em risco', 'Nao pode perde-los', 'Esfriando'. If someone asks what client they should visit you must search for the rfm_class 'Em risco'.

Question: {input}
### Response: 
"""
