
from flask import Flask, render_template, request, redirect, url_for

import emag_db

app = Flask(__name__)

config = emag_db.read_config()
user_id, username, password = emag_db.read_admins(config)

users = {
    username: password
    }

@app.route("/")
def first_function():
    print("S-a rulat cand apasam pe link")
    return render_template("login.html")


@app.route("/test")
def second_function():
    print("S-a rulat cand apasam pe link")
    return render_template("test.html")


@app.route("/login", methods=["POST"])
def web_login():
    user = request.form['username']
    passwrd = request.form['password']

    if user in users.keys():
        if passwrd == users[user]:
            data = emag_db.read_products(config)
            return render_template("home.html", data=data)

    return render_template("login.html")


@app.route("/add_products", methods=["POST"])
def add_new_product():
    name = request.form['product_name']
    store = request.form['store']
    price = request.form['price']
    new_product = emag_db.add_product(config, name, price, store)
    data = emag_db.read_products(config)
    return render_template("home.html", data=data)


@app.route("/delete_product", methods=["POST"])
def delete_product():
    name = request.form['product_name']
    emag_db.delete_product(config, name)
    data = emag_db.read_products(config)
    return render_template("home.html", data=data)


@app.route("/update_price", methods=["POST"])
def update_price():
    name = request.form['product_name']
    new_price = request.form['new_price']
    emag_db.update_price(config, name, new_price)
    data = emag_db.read_products(config)
    return render_template("home.html", data=data)


@app.route("/most_expensive", methods=["GET"])
def most_expensive():
    most_expensive_product = emag_db.get_most_expensive_product(config)
    data = emag_db.read_products(config)
    return render_template("home.html", data=data, most_expensive=most_expensive_product)

if __name__ == '__main__':
    app.run()