from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify, request)

# Get all of a user's order preferences
@app.route('/findRestaurant/<restaurant_id>', methods=['GET'])
def findRestaurant(restaurant_id):
    conn, mycursor = db_acq_lock()
    query = """SELECT r.restaurant_name, r.location, r.rating, r.website, r.food_types
               FROM Restaurant r
                WHERE r.restaurant_id = %s"""
    params = (str(restaurant_id), )
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
    
    db_rel_lock()

    return jsonify({'restaurant':restaurant})

@app.route('/newRestaurant', methods=['POST'])
def createRestaurant():
    conn, mycursor = db_acq_lock()
    print("hellooo")
    data = request.json;
    print(data)
    query = """INSERT INTO Restaurant(restaurant_id, restaurant_name, location, rating, website, food_types)
               VALUES(%s, %s, %s, %s, %s, %s) """
    params = (str(data['crid']), str(data['rname']), str(data['rloc']),
                str(data['rrate']), str(data['rsite']), str(data['rcuis']))
    print(query);
    mycursor.execute(query, params)

    # restaurant = []
    # for (restaurant_name, location, rating, website, food_types) in mycursor:
    #     restaurant.append({
    #         'location': location,
    #         'rating': rating,
    #         'website': website,
    #         'restaurant_name': restaurant_name,
    #         'food_types': food_types
    #     })
    # return jsonify({'restaurant':restaurant})
    conn.commit()
    db_rel_lock()
    print("done")
    return "Done!!"
