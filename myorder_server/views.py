from myorder_server import app
from flask import (render_template)

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return render_template("index.html")

@app.route('/user/<user_id>', methods=['GET'])
def get_userpage(user_id):
    return render_template("userpage.html", user_id=user_id)

@app.route('/restaurant/<restaurant_id>', methods=['GET'])
def get_restaurantpage(restaurant_id):
    return render_template("restaurantpage.html", restaurant_id=restaurant_id)

@app.route('/search', methods=['GET'])
def get_search():
    return render_template("search.html")

@app.route('/login', methods=['GET'])
def get_signin():
    return render_template("signin.html")

@app.route('/restaurant', methods=['GET'])
def serve_rest_index():
    return render_template("restaurant.html")

@app.route('/orders', methods=['GET'])
def serve_orders_index():
    return render_template("orders.html")

@app.route('/users/', methods=['GET'])
def get_user():
    return render_template("users.html")

@app.route('/stats', methods=['GET'])
def get_stats():
    return render_template("stats.html")

@app.route('/menuitem', methods=['GET'])
def get_menu():
    return render_template("menuitem.html")

@app.route('/feedback', methods=['GET'])
def get_feedback():
    return render_template("feedback-create.html")

from myorder_server.api import db, orders, restaurant, stats, user, menuitem, feedback
