from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json
from flask import (render_template)

@app.route('/stats/get', methods=['GET'])
def getLocationRatings():
    print("HELLO")
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
                    SELECT Restaurant.location, AVG(Feedback.rating) as average_rating
                    FROM Feedback INNER JOIN Restaurant ON Feedback.restaurant_id=Restaurant.restaurant_id
                    GROUP BY Restaurant.location
                    Order BY average_rating DESC
                    """)
    locations = []
    average_feedback = []
    for (location, average_rating) in cursor:
        locations.append({
                'location' : location,
                'rating' : str(average_rating)
        })

    db_rel_lock()
    return jsonify({'locations' : locations})