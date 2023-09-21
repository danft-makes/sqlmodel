SYSTEM_RULES="You will try to write an accurate and brief instru" 
HARD_RULE="Be #TODO"

prompt_maker = False #TODO
if prompt_maker==True:
    metavars="""{SYSTEM_CONTEXT}"""
    text1="""{SYSTEM_RULES}"""
    text2="""{HARD_RULE}"""
else:
    metavars="""Table manager columns: [manager_id,name,performance_class]
    Table sales columns: [sale_id,sale_date,quantity,total_price,customer_id,branch_id,product_id]
    Table customer has columns: [customer_id,creation_date,rfm_class,name,phone,last_purchase_date,city]
    Table branch columns: [branch_id,city,manager_id]
    Table product columns: [product_id,name,creation_date,description,category]
    Foreign keys: [sales.customer_id = customer.customer_id, sales.branch_id = branch.branch_id, sales.product_id = product.product_id, branch.manager_id = manager.manager_id]"""
    text1="""Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc...).
    If the question does not seem related to the database, just return "I don't know".
    If the user asks for a list of clients that he HAS to visit then you should look at the table customer.rfm_class, important values are 'Em Risco','Esfriando','Nao pode perder'."""
    text2="""Answer ONLY a sqlite query that answers the question."""

instruction=metavars+'\n'+text1+'\n'+text2
db_info="""∣ manager : manager_id , name , performance_class ∣ sales : sale_id , sale_date , quantity , total_price , customer_id , branch_id , product_id ∣ customer : customer_id , creation_date , rfm_class , name , phone , last_purchase_date , city ∣ branch : branch_id , city , manager_id ∣ product : product_id , name , creation_date , description , category ∣ sales.customer_id = customer.customer_id ∣ sales.branch_id = branch.branch_id ∣ sales.product_id = product.product_id ∣ branch.manager_id = manager.manager_id ∣"""
