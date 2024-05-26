import json
import psycopg2 as ps

def read_config(path: str = "config.json"):
    with open(path, "r") as f:
        config = json.loads(f.read())

    return config


def read_admins(config: dict, table: str = "emag.emag_admin"):

    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select * from {table}"
            cursor.execute(sql_query)
            users = cursor.fetchone()
            print()
            return users


def read_products(config: dict, table: str= "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select name, store, price from {table}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            products_list = []
            for item in products:
                products_list.append(dict(zip(columns, item)))

            return products_list


def add_product(config: dict, table: str= "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT name FROM {table}")
            all_products = [product[0] for product in cursor.fetchall()]
            new_prod = input("Add the new product: name store price \n")
            new_prod = new_prod.split(" ")
            if new_prod[0] not in all_products:
                cursor.execute(f"INSERT INTO emag.products(name, store, price) VALUES ('{new_prod[0]}', '{new_prod[1]}', '{new_prod[2]}')")
            else:
                print("Produsul deja exista")



if __name__ == '__main__':
    config = read_config()
    admins = read_admins(config)
    products = read_products(config)
    new_prod = add_product(config)