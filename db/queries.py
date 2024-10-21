CREATE_TABLE_STORE = """
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    product_id INTEGER,
    name_product varchar(255),
    size varchar(255),
    price varchar(255),
    photo TEXT
)
"""

CREATE_TABLE_PRODUCT_DETAILS = """
CREATE TABLE IF NOT EXISTS product_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    category varchar(255),
    info_product varchar(255)
)
"""

CREATE_TABLE_COLLECTION_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS collection_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        collection varchar(255)
    )
"""


INSERT_STORE_QUERY = """
    INSERT INTO store (product_id, name_product, size, price, photo)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_DETAILS_QUERY = """
    INSERT INTO product_details (product_id, category, info_product)
    VALUES (?, ?, ?)
"""

INSERT_COLLECTION_QUERY = """
    INSERT INTO collection_products (product_id, collection)
    VALUES (?, ?)
"""

INPUT_PRODUCTS_QUERY = """
    SELECT * FROM store
    JOIN product_details ON store.product_id = product_details.product_id
    JOIN collection_products ON store.product_id = collection_products.product_id
"""

GET_ALL_PRODUCTS = """
    SELECT s.id, s.product_id, s.name_product, s.size, s.price,
    s.photo, ds.category, ds.info_product, cs.collection
    FROM store s
    INNER JOIN product_details ds ON s.product_id = ds.product_id
    INNER JOIN collection_products cs ON s.product_id = cs.product_id
"""