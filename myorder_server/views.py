from myorder_server import app
from flask import (render_template)

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return render_template("index.html", flask_token="Hello   world")

@app.route('/restaurant', methods=['GET'])
def serve_rest_index():
    return render_template("restaurant.html", flask_token="Hello   world")

@app.route('/orders', methods=['GET'])
def serve_orders_index():
    return render_template("orders.html", flask_token="Hello   world")

@app.route('/users', methods=['GET'])
def get_user():
    return render_template("users.html", flask_token="tok")

@app.route('/stats', methods=['GET'])
def get_stats():
    return render_template("stats.html", flask_token = "tok")


from myorder_server.api import db, orders, restaurant, stats, user
