import sqlite3

from db import queries

db = sqlite3.connect('db/store.sqlite3')
db.row_factory = sqlite3.Row
cursor = db.cursor()


async def sql_create():
    if db:
        print('data base is ready!')
    
    
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_PRODUCT_DETAILS)
    cursor.execute(queries.CREATE_TABLE_COLLECTION_PRODUCTS)

async def sql_insert_product(product_id, product_name, size, price, photo, category, info_product, collection):
    cursor.execute(queries.INSERT_DETAILS_QUERY, (product_id, category, info_product))
    cursor.execute(queries.INSERT_STORE_QUERY, (product_id, product_name, size, price, photo))
    cursor.execute(queries.INSERT_COLLECTION_QUERY, (product_id, collection))
    db.commit()

def fetch_all_products():
    products = cursor.execute(queries.GET_ALL_PRODUCTS).fetchall()
    products_list = [dict(product) for product in products]
    return products_list