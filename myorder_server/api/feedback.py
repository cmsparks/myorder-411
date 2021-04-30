from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json

# Create a feedback
@app.route('/feedback/<restaurant_id>+<user_id>+<content>+<rating>', methods=['CREATE'])
def api_create_feedback(restaurant_id, user_id, content, rating):
    conn, cursor = db_acq_lock()
    
    query = """INSERT INTO Feedback (restaurant_id, user_id, timestamp, content, rating)
        VALUES (%s, %s, %s, %s, %s)"""
    params = (restaurant_id, user_id, 0, content, rating)
    cursor.execute(query, params)

    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# Delete a feedback
@app.route('/feedback/<restaurant_id>+<user_id>', methods=['DELETE'])
def api_delete_feedback(restaurant_id, user_id):
    conn, cursor = db_acq_lock()
    
    query = """DELETE FROM Feedback WHERE 
        restaurant_id = %s AND user_id = %s"""
    params = (restaurant_id, user_id)
    cursor.execute(query, params)

    conn.commit() 
    db_rel_lock()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
