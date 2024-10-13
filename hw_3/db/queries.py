CREATE_TABLE_STORE = """
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY_KEY AUTOINCREMENT ,
    name_product varchar(255),
    size varchar(255),
    category varchar(255),
    price varchar(255),W
    photo TEXT
)
"""


INSERT_STORE_QUERY = """
    INSERT INTO store (name, size, price, photo)
    VALUES (?, ?, ?, ?)
"""