metavars="""Table inventory columns: [inventory_id,product_id,branch_id,quantity]
Table sales columns: [sale_id,sale_date,customer_id,branch_id,product_id,quantity,total_price]
Table customer columns: [branch_id,manager_id,city]
Table branch columns: [branch_id,manager_id,city]
Table product columns: [product_id,name,category,creation_date,description]
JOINS: [sales.customer_id = customer.customer_id, sales.branch_id = branch.branch_id, sales.product_id = product.product_id, inventory.product_id = product.product_id, inventory.branch_id = branch.branch_id, branch.manager_id = manager.manager_id]"""
text1="""Never query for all the columns from a specific table, only ask for the relevant columns given the question.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc...).
If the question does not seem related to the database, just return "I don't know"."""
text2="""Answer only a sqlite query that answers the question"""
