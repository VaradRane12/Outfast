import sqlite3

# Path to the uploaded database file
db_path = "store2.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the 'products' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)
# Check the schema of the 'products' table (if it exists)
schema = None
if ('products',) in tables:
    cursor.execute("PRAGMA table_info(products);")
    schema = cursor.fetchall()

# Check if there are any records in the 'products' table
records = None
if ('products',) in tables:
    cursor.execute("SELECT * FROM products LIMIT 5;")  # Fetch a few records
    records = cursor.fetchall()

# Close the connection
conn.close()

# Output the results
print(tables, schema, records)
