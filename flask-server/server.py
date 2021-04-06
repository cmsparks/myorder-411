from flask import (Flask, render_template)

app = Flask(__name__)
 
 
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return render_template("index.html", flask_token="Hello   world")

@app.route('/apitest', methods=['GET'])
def test_api_route():
    return "This is a test"

app.run(host='0.0.0.0',port=8080)
