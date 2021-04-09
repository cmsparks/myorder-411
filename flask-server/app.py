from flask import (Flask, render_template, jsonify, request)
import db
app = Flask(__name__)

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return render_template("index.html", flask_token="Hello   world")

@app.route('/restaurant', methods=['GET'])
def serve_rest_index():
    return render_template("restaurant.html", flask_token="Hello   world")

@app.route('/orders', methods=['GET'])
def serve_orders_index():
    return render_template("orders.html", flask_token="Hello   world")

from api import orders, restaurant

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
