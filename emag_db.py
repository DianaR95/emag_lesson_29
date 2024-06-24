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


def add_product(config: dict, name: str, price: str, store: str, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT name FROM {table}")
            all_products = [product[0] for product in cursor.fetchall()]
            if name not in all_products:
                cursor.execute(f"INSERT INTO {table} (name, store, price) VALUES ('{name}', '{store}', '{price}')")
                conn.commit()
            else:
                print("Produsul deja exista")


def delete_product(config: dict, name: str, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table} WHERE name = %s", (name,))
            conn.commit()


def update_price(config: dict, name: str, new_price: str, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET price = %s WHERE name = %s", (new_price, name))
            conn.commit()


def get_most_expensive_product(config: dict, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"SELECT name FROM {table} ORDER BY price DESC LIMIT 1"
            cursor.execute(sql_query)
            product = cursor.fetchone()
            if product:
                return product[0]
            else:
                return None


if __name__ == '__main__':
    config = read_config()
    admins = read_admins(config)
    products = read_products(config)
    new_prod = add_product(config)