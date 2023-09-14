# langchain

This project uses a local language model (llm) for text to SQL tasks. The main scripts in this project are `db.py` and `sql.py`.

## db.py

This script is responsible for creating and populating a SQLite database. It uses the `faker` library to generate dummy data for the database. The database consists of several tables including `product`, `branch`, `customer`, `inventory`, and `sales`. Each table is populated with appropriate dummy data.

## sql.py

This script uses the database created by `db.py` and a local llm for text to SQL tasks. It uses the `langchain` library for interacting with the database and the llm. The script takes a query as input and returns the result of the query.

## Prompts

We are still working on the prompts for the llm. The current prompt template is defined in `sql.py` and includes instructions for the llm on how to interact with the database.

Please note that this project is still under development and more features will be added in the future.
