import sqlite3
import json
from faker import Faker

# Create a new SQLite database
def create_query_db() -> None:
    conn = sqlite3.connect('query.db')
    c = conn.cursor()

    # Creating the table
    c.execute('''CREATE TABLE IF NOT EXISTS trio 
                 (id INTEGER PRIMARY KEY, query TEXT NOT NULL, gold TEXT NOT NULL)''')


    # Populate the analysis table
    populate_analysis_table(c)

    conn.commit()
    conn.close()

def create_analysis_db() -> None:
    conn = sqlite3.connect('analysis.db')
    c = conn.cursor()

    # Tables from the create_db function
    c.execute('''CREATE TABLE IF NOT EXISTS product 
                 (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, creation_date DATE NOT NULL, description TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS branch 
                 (branch_id INTEGER PRIMARY KEY, manager_name TEXT NOT NULL, city TEXT NOT NULL, branch_name TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS customer 
                 (customer_id INTEGER PRIMARY KEY, customer_age INTEGER NOT NULL, creation_date DATE NOT NULL, rfm_class TEXT NOT NULL, name TEXT NOT NULL, city TEXT NOT NULL, phone TEXT NOT NULL, last_purchase_date DATE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS inventory 
                 (inventory_id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL, branch_id INTEGER NOT NULL, quantity INTEGER NOT NULL,
                 FOREIGN KEY(product_id) REFERENCES product(product_id),
                 FOREIGN KEY(branch_id) REFERENCES branch(branch_id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS sales 
                 (sale_id INTEGER PRIMARY KEY, sale_date DATE NOT NULL, customer_id INTEGER NOT NULL, branch_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, total_price REAL NOT NULL,
                 FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
                 FOREIGN KEY(branch_id) REFERENCES branch(branch_id),
                 FOREIGN KEY(product_id) REFERENCES product(product_id))''')

    # Additional analysis table
    c.execute('''CREATE TABLE IF NOT EXISTS analysis 
                 (id INTEGER PRIMARY KEY, query TEXT NOT NULL, response TEXT NOT NULL, gold TEXT NOT NULL)''')

    conn.commit()
    conn.close()

def populate_analysis_table(cursor):
    with open('queries.json', 'r', encoding='latin-1') as f:
        queries = json.load(f)
        for query in queries:
            cursor.execute('INSERT INTO trio (query, gold) VALUES (?, ?)',
                           (query['query'], query['gold']))




# Populate the database with dummy data
def populate_db() -> None:
    conn = sqlite3.connect('analysis.db')
    c = conn.cursor()
    fake = Faker()

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
