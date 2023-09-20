import sqlite3
import json
from faker import Faker

# Create a new SQLite database
def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn.cursor()

def create_table(c, table_name, columns):
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} {columns}''')

def create_query_db() -> None:
    c = connect_to_db('queries.db')

    # Creating the table
    create_table(c, 'trio', '(id INTEGER PRIMARY KEY, query TEXT NOT NULL, gold TEXT NOT NULL)')

    # Populate the analysis table
    populate_queries_db(c)

    conn.commit()
    conn.close()

def create_analysis_db() -> None:
    c = connect_to_db('analysis.db')

    # Tables from the create_db function
    create_table(c, 'product', '(product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, creation_date DATE NOT NULL, description TEXT)')
    create_table(c, 'branch', '(branch_id INTEGER PRIMARY KEY, manager_name TEXT NOT NULL, city TEXT NOT NULL, branch_name TEXT NOT NULL)')
    create_table(c, 'customer', '(customer_id INTEGER PRIMARY KEY, customer_age INTEGER NOT NULL, creation_date DATE NOT NULL, rfm_class TEXT NOT NULL, name TEXT NOT NULL, city TEXT NOT NULL, phone TEXT NOT NULL, last_purchase_date DATE NOT NULL)')
    create_table(c, 'inventory', '(inventory_id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL, branch_id INTEGER NOT NULL, quantity INTEGER NOT NULL, FOREIGN KEY(product_id) REFERENCES product(product_id), FOREIGN KEY(branch_id) REFERENCES branch(branch_id))')
    create_table(c, 'sales', '(sale_id INTEGER PRIMARY KEY, sale_date DATE NOT NULL, customer_id INTEGER NOT NULL, branch_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, total_price REAL NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id), FOREIGN KEY(branch_id) REFERENCES branch(branch_id), FOREIGN KEY(product_id) REFERENCES product(product_id))')

    # Additional analysis table
    create_table(c, 'analysis', '(id INTEGER PRIMARY KEY, query TEXT NOT NULL, response TEXT NOT NULL, gold TEXT NOT NULL)')

    conn.commit()
    conn.close()

def populate_queries_db(cursor):
    with open('queries.json', 'r', encoding='latin-1') as f:
        queries = json.load(f)
        for query in queries:
            cursor.execute('INSERT INTO trio (query, gold) VALUES (?, ?)',
                           (query['query'], query['gold']))




# Populate the database with dummy data
def sync_with_queries_db():
    conn_query = sqlite3.connect('queries.db')
    c_query = conn_query.cursor()
    c_query.execute('SELECT * FROM trio')
    rows = c_query.fetchall()

    conn_analysis = sqlite3.connect('analysis.db')
    c_analysis = conn_analysis.cursor()
    for row in rows:
        c_analysis.execute('INSERT INTO analysis (id, query, response, gold) VALUES (?, ?, ?, ?)', (row[0], row[1], '', row[2]))

    conn_query.close()
    conn_analysis.commit()
    conn_analysis.close()

def populate_db() -> None:
    conn = sqlite3.connect('analysis.db')
    c = conn.cursor()
    fake = Faker()
    sync_with_queries_db()

    branch_names = ['North Branch', 'South Branch', 'East Branch', 'West Branch', 'Central Branch']
    common_cities = [fake.city() for _ in range(5)]  # 5 common cities

    # Inserting dummy data into the tables
    products = {
        'Electronics': ['Phone', 'Laptop', 'Headphones', 'Charger', 'Camera'],
        'Clothing': ['Shirt', 'Pants', 'Shoes', 'Jacket', 'Socks'],
        'Food': ['Bread', 'Milk', 'Cheese', 'Eggs', 'Butter']
    }

    customer_creation_dates = {}

    for _ in range(100):
        category = fake.random_element(elements=('Electronics', 'Clothing', 'Food'))
        product_name = fake.random_element(elements=products[category])

        c.execute('INSERT INTO product (name, category, creation_date, description) VALUES (?, ?, ?, ?)',
                  (product_name, category, fake.date(), fake.text()))

        c.execute('INSERT INTO branch (manager_name, city, branch_name) VALUES (?, ?, ?)',
                  (fake.name(), fake.random_element(common_cities), fake.random_element(branch_names)))

        creation_date = fake.date()
        c.execute('INSERT INTO customer (customer_age, creation_date, rfm_class, name, city, phone, last_purchase_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (fake.random_int(min=18, max=80), creation_date, fake.random_element(elements=('A', 'B', 'C')), fake.name(), fake.random_element(common_cities), fake.phone_number(), fake.date()))

        customer_id = c.lastrowid
        customer_creation_dates[customer_id] = creation_date

    for _ in range(500):
        customer_id = fake.random_int(min=1, max=100)
        sale_date = fake.date()

        # Ensure sale date does not precede customer creation date
        while sale_date <= customer_creation_dates[customer_id]:
            sale_date = fake.date()

        c.execute('INSERT INTO sales (sale_date, customer_id, branch_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?)',
                  (sale_date, customer_id, fake.random_int(min=1, max=100), fake.random_int(min=1, max=100), fake.random_int(min=1, max=10), fake.random_number(digits=5)))

        c.execute('INSERT INTO inventory (product_id, branch_id, quantity) VALUES (?, ?, ?)',
                  (fake.random_int(min=1, max=100), fake.random_int(min=1, max=100), fake.random_int(min=1, max=1000)))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_query_db()
    create_analysis_db()
    populate_db()
    print("Database created and populated!")
