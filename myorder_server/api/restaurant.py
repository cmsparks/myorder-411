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

    conn.commit()
    db_rel_lock()
    print("done")
    return "Done!!"

@app.route('/deleteRestaurant/<restaurant_id>', methods=['POST'])
def deleteRestaurant(restaurant_id):
    conn, mycursor = db_acq_lock()
    query = """DELETE FROM Restaurant
               WHERE restaurant_id = %s """
    params = (str(restaurant_id), )
    print(query);
    mycursor.execute(query, params)

    conn.commit()
    db_rel_lock()
    print("done")
    return "DELETED!"

@app.route('/editRestaurant', methods=['POST'])
def editRestaurant():
    conn, mycursor = db_acq_lock()
    print("hellooo")
    data = request.json;
    print(data)
    query = """UPDATE Restaurant
                SET restaurant_name = %s, location = %s, 
                rating = %s, website = %s, food_types = %s
                WHERE restaurant_id = %s """
    params = (str(data['rname']), str(data['rloc']),
                str(data['rrate']), str(data['rsite']), str(data['rcuis']), str(data['crid']))
    print(query);
    mycursor.execute(query, params)

    conn.commit()
    db_rel_lock()
    print("done")
    return "Done!"

@app.route('/findRestaurant/<restaurant_id>/feedback', methods=['GET'])
def getRestaurantFeedback(restaurant_id):
    conn, mycursor = db_acq_lock()
    # print(data)
    query = """
                SELECT f.content, f.user_id, f.restaurant_id, f.timestamp, f.rating, u.username
                FROM Feedback f JOIN User u ON u.user_id = f.user_id
                WHERE restaurant_id = %s
            """
    params = (restaurant_id, )
    mycursor.execute(query, params)

    feedback = []
    
    for pair in mycursor:
        feedback.append({
            "content": pair[0],
            "user_id": pair[1],
            "restaurant_id": pair[2],
            "timestamp": pair[3],
            "rating": pair[4],
            "username": pair[5]
        })

    db_rel_lock()
    return jsonify({"feedback": feedback})


@app.route('/advRestaurant', methods=['GET'])
def advQueryRestaurant():
    conn, mycursor = db_acq_lock()
    print("hellooo")
    # print(data)
    query = """
                SELECT f.restaurant_id, Count(*) as c
                FROM Feedback f
                JOIN Restaurant r ON r.restaurant_id = f.restaurant_id
                WHERE r.rating > 3
                GROUP BY f.restaurant_id
                ORDER BY r.rating DESC
            """
    print(query);
    mycursor.execute(query)

    restaurants = {
        "list": []
    }
    # for (restaurant_name, location, rating, website, food_types) in mycursor:
    #     restaurant.append({
    #         'location': location,
    #         'rating': rating,
    #         'website': website,
    #         'restaurant_name': restaurant_name,
    #         'food_types': food_types
    #     })
    for pair in mycursor:
        restaurants["list"].append({
            "rid": pair[0],
            "rnum": pair[1]
        })
        
    print(restaurants)

    conn.commit()
    db_rel_lock()

    return jsonify({'data':restaurants})
    print("done")
    return "Done!"


@app.route('/search/restaurants/<search>', methods=['GET'])
def search_restaurant(search):
    print(search)
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
                  SELECT u.restaurant_id, u.restaurant_name, u.location, u.rating, u.website, u.food_types
                  FROM Restaurant u
                  WHERE u.restaurant_name LIKE "%"%s"%" 
                  """, (search,))

    restaurants = []
    for (rid, restaurant_name, location, rating, website, food_types) in cursor:
        print(restaurant_name)
        restaurants.append({
            'restaurant_id': rid,
            'location': location,
            'rating': rating,
            'website': website,
            'restaurant_name': restaurant_name,
            'food_types': food_types
        })
    db_rel_lock()
    return jsonify({'restaurant' : restaurants})
