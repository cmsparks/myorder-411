from flask import (Flask, render_template, jsonify)
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

@app.route('/findRestaurant/<restaurant_id>', methods=['GET'])
def findRestaurant(restaurant_id):
    conn, cursor = db.db_conn()
    query = """SELECT r.restaurant_name, r.location, r.rating, r.website, r.food_types
               FROM Restaurant r
                WHERE r.restaurant_id = %s"""
    params = (str(restaurant_id))
    cursor.execute(query, params)

    restaurant = []
    for (restaurant_name, location, rating, website, food_types) in cursor:
        restaurant.append({
            'location': location,
            'rating': rating,
            'website': website,
            'restaurant_name': restaurant_name,
            'food_types': food_types
        })
    
    cursor.close()
    conn.close()
    return jsonify({'restaurant':restaurant})


from api import orders

app.run(host='0.0.0.0',port=8080)
