from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify, request)
import json

# Get all of a user's order preferences
@app.route('/user/<user_id>/orders', methods=['GET'])
def api_user_orders(user_id):
    print("proc orders on uid: ", user_id)
    conn, cursor = db_acq_lock()
    orders = []
    query = """SELECT m.item_name, o.restaurant_id, m.item_price, m.item_desc, r.restaurant_name, o.notes
               FROM OrderPreferences o
                 JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
                 JOIN MenuItem m ON (o.item_name = m.item_name
                                        AND o.restaurant_id = m.restaurant_id)
                WHERE o.user_id = %s"""
    params = (str(user_id), )
    cursor.execute(query, params)
    for (item_name, restaurant_id, item_price, item_desc, restaurant_name, notes) in cursor:
        orders.append({
            'item_name': item_name,
            'restaurant_id': restaurant_id,
            'item_price': item_price,
            'item_desc': item_desc,
            'restaurant_name': restaurant_name,
            'notes': notes,
        })

    db_rel_lock()
    return jsonify({'orders':orders})

# Update a single order preference
@app.route('/user/<user_id>/orders/<restaurant_id>+<item_name>', methods=['PUT'])
def api_update_order(user_id, restaurant_id, item_name):
    print("proc orders on uid: ", user_id)
    conn, cursor = db_acq_lock()
   
    notes = request.data

    query = """UPDATE OrderPreferences SET
        notes = %s
        WHERE (user_id = %s AND (restaurant_id = %s AND item_name = %s))"""
    params = (notes, user_id, restaurant_id, item_name)
    cursor.execute(query, params)
    
    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# Create a new order preference
@app.route('/user/<user_id>/orders/<restaurant_id>+<item_name>', methods=['CREATE'])
def api_create_order(user_id, restaurant_id, item_name):
    conn, cursor = db_acq_lock()
   
    notes = request.data

    query = """INSERT INTO OrderPreferences (user_id, restaurant_id, item_name, notes)
    VALUES (%s, %s, %s, %s)"""
    params = (user_id, restaurant_id, item_name, notes)
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



# Delete a new order preference
@app.route('/user/orders/top', methods=['GET'])
def api_top_orderers():
    conn, cursor = db_acq_lock()
    
    query = """select u.username, u.user_id, count(*) as numOrders
    from OrderPreferences o join User u on u.user_id = o.user_id
    group by u.username, u.user_id
    order by numOrders DESC
    limit 100;"""
    cursor.execute(query)
    top = []
    
    for (username, uid, num_orders) in cursor:
        top.append({
            'username': username,
            'uid': uid,
            'num_orders': num_orders
        })

    db_rel_lock()
    
    return jsonify({'top':top})
