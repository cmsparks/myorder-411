from flask import (Flask, render_template, jsonify)
import mysql.connector
mydb = mysql.connector.connect(
    host= "34.67.0.57",
    user= "root",
    password= "1234",
    database = "one_data"
)

mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)
 
import mysql.connector
import random
mydb = mysql.connector.connect (
    host= "34.67.0.57",
    user= "root",
    password= "1234",
    database = "one_data"
)

mycursor = mydb.cursor(buffered=True)
 
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return render_template("index.html", flask_token="Hello   world")

@app.route('/orders', methods=['GET'])
def serve_orders_index():
    return render_template("orders.html", flask_token="Hello   world")

@app.route('/user/<user_id>/orders', methods=['GET'])
def api_user_orders(user_id):
    print("proc orders on uid: ", user_id)
    orders = []
    query = """SELECT m.item_name, m.item_price, m.item_desc, r.restaurant_name
               FROM OrderPreferences o
                 JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
                 JOIN MenuItem m ON (o.item_name = m.item_name
                                        AND o.restaurant_id = m.restaurant_id)
                WHERE o.user_id = %s"""
    params = (str(user_id), )
    mycursor.execute(query, params)
    for (item_name, item_price, item_desc, restaurant_name) in mycursor:
        orders.append({
            'item_name': item_name,
            'item_price': item_price,
            'item_desc': item_desc,
            'restaurant_name': restaurant_name
        })
    return jsonify({'orders':orders})

@app.route('/apitest', methods=['GET'])
def api_test():
    return "This is a test"

@app.route('/orders', methods=['GET'])
def serve_orders_index():
    return render_template("restaurant.html", flask_token="Hello   world")

@app.route('/findRestaurant/<restaurant_id>', methods=['GET'])
def findRestaurant(restaurant_id):
    query = """SELECT r.restaurant_name, r.location, r.rating, r.website, r.food_types
               FROM Restaurant r
                WHERE r.restaurant_id = %s"""
    params = (str(restaurant_id))
    mycursor.execute(query, params)

    restaurant = []
    for (restaurant_name, location, rating, website, food_types) in mycursor:
        restaurant.append({
            'location': location,
            'rating': rating,
            'website': website,
            'restaurant_name': restaurant_name,
            'food_types': food_types
        })
    return jsonify({'restaurant':restaurant})


app.run(host='0.0.0.0',port=8080)
