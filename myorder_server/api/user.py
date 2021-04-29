from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json
from flask import (render_template)

@app.route('/users/<user_id>', methods=['GET'])
def get_user_data(user_id):
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
                  SELECT *
                  FROM User u
                  WHERE u.user_id = %s
                  """, (user_id,))

    users = []
    for (user_id, username, email, password, full_name, tags) in cursor:
        users.append({
                'user_id' : user_id,
                'username' : username,
                'email' : email,
                'password' : password,
                'full_name' : full_name, 
                'tags' : tags
        })
    db_rel_lock()
    return jsonify({'users' : users})

@app.route('/users/update/<user_id>/<tags>', methods=['POST'])
def update_user_data(user_id, tags):
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
                UPDATE User
                SET tags = %s
                WHERE user_id = %s
                """, (tags, user_id,))
    conn.commit()
    db_rel_lock()
    return render_template("users.html", flask_token="tok")

@app.route('/users/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    print("Reached User Delete in app.py with id: " + user_id)
    conn, cursor = db_acq_lock()
    print("DELETING USER: " + user_id)

    res = cursor.execute("""  

                        DELETE
                        FROM User
                        WHERE user_id = %s
                         """, (user_id,))
    conn.commit()
    db_rel_lock()
    return render_template("users.html", flask_token="tok")

@app.route('/users/create/<username>/<email>/<password>/<full_name>/<tags>', methods=['POST'])
def create_user(username, email, password, full_name, tags):
    conn, cursor = db_acq_lock()
    re = cursor.execute("""
                SELECT u.user_id
                FROM User u
                """)
    
    user_id_list = set()
    total_list = set()
    count = 0
    for (user_id) in cursor:
        total_list.add(count)
        user_id_list.add(int(user_id[0]))
        count = count + 1
    diff = total_list - user_id_list
    
    id = 0
    if len(diff) < 2:
        id = max(user_id_list) + 1
    else:
        id = min(diff)

    print(id)
        
    res = cursor.execute("""
                    INSERT INTO User(user_id, username, email, password, full_name, tags)
                    VALUES (%s, %s, %s, %s, %s, %s )""", (id, username, email, password, full_name, tags,))

    conn.commit()
    db_rel_lock()
    return render_template("users.html", flask_token="tok")

@app.route('/users/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
        SELECT u.*
        from (SELECT user_id_2 as uid FROM Friends WHERE user_id_1 = %s
        UNION
        SELECT user_id_1 as uid FROM Friends WHERE user_id_2 = %s) as f JOIN User u ON u.user_id = f.uid;
                  """, (user_id, user_id))

    friends = []
    for (user_id, username, email, password, full_name, tags) in cursor:
        print(full_name)
        friends.append({
                'user_id' : user_id,
                'username' : username,
                'email' : email,
                'password' : password,
                'full_name' : full_name, 
                'tags' : tags
        })
    db_rel_lock()

    return jsonify({'friends': friends})

@app.route('/search/users/<search>', methods=['GET'])
def search_user(search):
    print(search)
    conn, cursor = db_acq_lock()
    res = cursor.execute("""
                  SELECT * 
                  FROM User u
                  WHERE u.full_name LIKE "%"%s"%" 
                  """, (search,))

    users = []
    for (user_id, username, email, password, full_name, tags) in cursor:
        print(full_name)
        users.append({
                'user_id' : user_id,
                'username' : username,
                'email' : email,
                'password' : password,
                'full_name' : full_name, 
                'tags' : tags
        })
    db_rel_lock()
    return jsonify({'users' : users})
