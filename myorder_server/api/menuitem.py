from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json

# Get all of a restaurants menu items
@app.route('/menuitems/<restaurant_id>/menu', methods=['GET'])
def api_get_restaurant_menu(restaurant_id):
    print("proc menuitems on rid: ", restaurant_id)
    conn, cursor = db_acq_lock()
    menuitems = []
    # print("\n\n\nGIMME QUERRY\n\n\n")
    query = """SELECT mi.item_name, r.restaurant_id, mi.item_price, mi.item_desc, r.restaurant_name
               FROM Restaurant r JOIN MenuItem mi on r.restaurant_id = mi.restaurant_id
               WHERE r.restaurant_id = %s"""
    params = (str(restaurant_id), )
    cursor.execute(query, params)
    for (item_name, restaurant_id, item_price, item_desc, restaurant_name) in cursor:
        menuitems.append({
            'item_name': item_name,
            'restaurant_id': restaurant_id,
            'item_price': item_price,
            'item_desc': item_desc,
            'restaurant_name': restaurant_name
        })

    db_rel_lock()
    return jsonify({'menuitems':menuitems})

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
@app.route('/menuitem/<restaurant_id>+<item_name>+<item_price>+<item_description>', methods=['CREATE'])
def api_create_order(restaurant_id, item_name, item_price, item_desc):
    conn, cursor = db_acq_lock()
    
    query = """INSERT INTO MenuItem (restaurant_id, item_name, item_price, item_desc)
    VALUES (%s, %s, %f, %s)"""
    params = (restaurant_id, item_name, item_price, item_desc)
    cursor.execute(query, params)
    
    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# Delete a new order preference
@app.route('/menuitem/<restaurant_id>+<item_name>', methods=['DELETE'])
def api_delete_order(restaurant_id, item_name):
    conn, cursor = db_acq_lock()
    
    query = """DELETE FROM MenuItem 
        WHERE (restaurant_id = %s AND item_name = %s)"""
    params = (restaurant_id, item_name)
    cursor.execute(query, params)
    
    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
