from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json

# Get all of a user's order preferences
@app.route('/user/<user_id>/orders', methods=['GET'])
def api_user_orders(user_id):
    print("proc orders on uid: ", user_id)
    conn, cursor = db_acq_lock()
    orders = []
    query = """SELECT m.item_name, o.restaurant_id, m.item_price, m.item_desc, r.restaurant_name
               FROM OrderPreferences o
                 JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
                 JOIN MenuItem m ON (o.item_name = m.item_name
                                        AND o.restaurant_id = m.restaurant_id)
                WHERE o.user_id = %s"""
    params = (str(user_id), )
    cursor.execute(query, params)
    for (item_name, restaurant_id, item_price, item_desc, restaurant_name) in cursor:
        orders.append({
            'item_name': item_name,
            'restaurant_id': restaurant_id,
            'item_price': item_price,
            'item_desc': item_desc,
            'restaurant_name': restaurant_name
        })

    db_rel_lock()
    return jsonify({'orders':orders})

# Update a single order preference
@app.route('/user/<user_id>/orders/<restaurant_id>+<item_name>', methods=['POST'])
def api_update_order(user_id):
    print("proc orders on uid: ", user_id)
    conn, cursor = db_acq_lock()
    
    #update
    
    conn.commit() 
    db_rel_lock()
    return jsonify({'orders':orders})

# Create a new order preference
@app.route('/user/<user_id>/orders/<restaurant_id>+<item_name>', methods=['CREATE'])
def api_create_order(user_id, restaurant_id, item_name):
    conn, cursor = db_acq_lock()
    
    query = """INSERT INTO OrderPreferences (user_id, restaurant_id, item_name)
    VALUES (%s, %s, %s)"""
    params = (user_id, restaurant_id, item_name)
    cursor.execute(query, params)
    
    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# Delete a new order preference
@app.route('/user/<user_id>/orders/<restaurant_id>+<item_name>', methods=['DELETE'])
def api_delete_order(user_id, restaurant_id, item_name):
    conn, cursor = db_acq_lock()
    
    query = """DELETE FROM OrderPreferences 
        WHERE (user_id = %s AND (restaurant_id = %s AND item_name = %s))"""
    params = (user_id, restaurant_id, item_name)
    cursor.execute(query, params)
    
    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
