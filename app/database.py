import sqlite3

# create a connection
connection = sqlite3.connect("shipment.db")
# create a cursor for execution
cursor = connection.cursor()

# 1. Create a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER, 
                content TEXT, 
                weight REAL, 
                status TEXT)
    """
)

# 2. Add shipment data into the data
cursor.execute(
    """
    INSERT INTO shipments
        VALUES (124, "basalt", 17.3, "in_transit")
    """
)

connection.commit()

# close the connection
connection.close()